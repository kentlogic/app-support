select
       date_part('month', tickets_ticket.date_added::date) as month,
       ticket_code,
       date_added,
       count(ticket_id)
from tickets_ticket
    group by 1, 2, 3
    order by date_added asc

drop database infohub_db
grant postgres to kent