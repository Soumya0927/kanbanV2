import weasyprint
import jinja2
from celery import Celery
from flask import current_app
from models import db, User, List, Card
from celery.schedules import crontab
from gen_email import send_email
import data_access
import os

celery = Celery("App job")


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(*args, **kwargs)


@celery.task()
def export_list(user_id, lid):
    cards = Card.query.filter_by(
        list_id=lid).all()
    cards = list(cards)
    cur_list = List.query.filter_by(user_id=user_id, lid=lid).first()
    listname = str(cur_list.list_name)
    user = User.query.filter_by(id=user_id).first()
    email_address = str(user.email)
    if len(cards) == 0:
        send_email(email_address, "Status of your Download List",
                   "The list id you specified may not exist or may not contain any cards and therefore we have not attached the CSV file.")
        return
    with open(r"list_" + str(user.id) + str(cur_list.list_name) + ".csv", "w") as f:
        f.write("Card Title,Card content,Card Deadline,Card Completed \n")
        for item in cards:
            if item.flag == '1':
                complete = 'Yes'
            else:
                complete = 'No'
            # timestamp = str(item.tracker_timestamp)
            thing = "{card_title},{content},{deadline},{done}\n"
            print(thing)
            f.write(thing.format(card_title=item.card_title,
                                 content=item.content, deadline=item.deadline, done=complete))
            f.flush()
        f.close()
    filename = "list_" + str(user.id) + str(cur_list.list_name) + ".csv"
    send_email(email_address, "Status of your Download List",
               f"Your download has been successfully completed for the list {listname}. You can find your download attached in this email.",
               filename)
    os.remove(filename)


@celery.task()
def export_card(user_id, cid):
    card = data_access.get_card_by_id(cid)
    # card = Card.query.filter_by(cid=cid).first()
    cardname = str(card.card_title)
    '''records = list(records)'''
    cur_list = List.query.filter_by(lid=card.list_id).first()
    user = User.query.filter_by(id=user_id).first()
    email_address = str(user.email)
    if not card:
        send_email(email_address, "Status of your Download Card",
                   "The card id you specified does not exist, therefore we have not attached the CSV file.")
        return
    with open(r"card_" + str(card.cid) + str(cur_list.list_name) + str(user.id) + ".csv", "w") as f:
        f.write(
            "Card Title,List belongs to,Card content,Card Deadline,Completed,Created Time,Last Updated \n")
        if card.flag == '1':
            complete = 'Yes'
        else:
            complete = 'No'
        thing = "{card_title},{list_belongs_to},{content},{deadline},{done},{created},{last_update}\n"
        print(thing)
        f.write(thing.format(card_title=card.card_title, list_belongs_to=cur_list.list_name,
                             content=card.content, deadline=card.deadline, done=complete, created=card.card_created,
                             last_update=card.last_change))
        f.flush()
        f.close()
    filename = "card_" + str(card.cid) + \
               str(cur_list.list_name) + str(user.id) + ".csv"
    send_email(email_address, "Status of your Download Card",
               f"Your download has been successfully completed for card {cardname}. You can find your download attached in this email.",
               filename)
    os.remove(filename)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #    10, generate_daily_report.s(), name='Daily ')

    sender.add_periodic_task(
        crontab(hour=15, minute=52), generate_daily_report.s(), name='Daily ')
    # crontab(hour=16, minute=2)
    # sender.add_periodic_task(5, generate_daily_report(), name='Daily ')
    # sender.add_periodic_task(crontab(hour=18, minute=11), test.s(user.email, 'hello'))


@celery.on_after_finalize.connect
def setup_monthly_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #    10, generate_monthly_report.s(), name='Pdf Progress Report')

    sender.add_periodic_task(
        crontab(hour=15, minute=53, day_of_month=15), generate_monthly_report.s(), name='Pdf Progress Report')
    # sender.add_periodic_task(crontab(hour=22, minute=18, day_of_month=13),
    #                          generate_daily_report(), name='Daily ')


@celery.task()
def generate_daily_report():
    users = User.query.all()
    for user in users:
        test.delay(user.email)


@celery.task()
def generate_monthly_report():
    users = User.query.all()
    for user in users:
        generate_dashboard_report_html.delay(user.email)


@celery.task()
def test(email):
    user = User.query.filter_by(email=email).first()
    name_user = str(user.username)
    lists = data_access.get_list_by_userId(user.id)
    # lists = List.query.filter_by(user_id=user.id).all()
    count = 0
    for each in lists:
        cards = Card.query.filter_by(list_id=each.lid).all()
        for c in cards:
            if c.flag == '0':
                count += 1
    send_email(email, "Daily Reminder",
               f"Dear {name_user}, You have {count} tasks pending. Update the status of your completion")


@celery.task()
def generate_dashboard_report_html(email):
    user = User.query.filter_by(email=email).first()
    lists = data_access.get_list_by_userId(user.id)
    # lists = List.query.filter_by(user_id=user.id).all()
    d = {}
    for each in lists:
        d[each.list_name] = []
        cards = Card.query.filter_by(list_id=each.lid).all()
        for c in cards:
            d[each.list_name].append({"cid": c.cid, "card_title": c.card_title,
                                      "content": c.content, "deadline": c.deadline, "flag": c.flag})
    print(d)
    # data = {'username': "hello", 'get_cards': d}
    # users = User.query.fi
    # data = {current_user.username, d}

    a = None
    with open("report.html") as f:
        report_template = jinja2.Template(f.read())
        a = report_template.render(name=str(user.username), get_cards=d)
        f.close()
    b = weasyprint.HTML(string=a)
    name = str(user.id) + "_dashboardreport.pdf"
    b.write_pdf(target=name)
    name_user = str(user.username)
    print(email)
    send_email(email, "Monthly Progress Report",
               f"Dear {name_user}, please find attached your monthly progress and usage report. We hope to receive your continued support.",
               name)
    os.remove(name)
