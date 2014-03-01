truncate tournament_slots_results;
insert into tournament_slots_results (season, slot, strongseed, weakseed, winning_team_id, losing_team_id) (select season, slot, strongseed, weakseed, null, null from tournament_slots);
-- update tournament_slots_results set winning_team_id = null, losing_team_id = null;
-- select * from tournament_slots_results where season = 'A';
-- select * from tournament_results where season = 'A' order by day_num, winning_team_id;
-- select slots.*, tr.winning_team_id, tr.losing_team_id

update tournament_slots_results res set winning_team_id = tr.winning_team_id, losing_team_id = tr.losing_team_id
from tournament_slots_results as slots
left join tournament_seeds as sts on sts.seed = slots.strongseed and slots.season = sts.season
left join tournament_seeds as wts on wts.seed = slots.weakseed and slots.season = wts.season
left join tournament_results as tr on 
(
tr.winning_team_id = sts.team_id
and tr.losing_team_id = wts.team_id
and sts.season = tr.season 
and wts.season = tr.season
) 
or 
(
wts.team_id = tr.winning_team_id 
and sts.team_id = tr.losing_team_id 
and wts.season = tr.season 
and sts.season = tr.season
)
where res.season = slots.season and res.slot = slots.slot;




-- this is an update to fix any qualifier
update tournament_slots_results res set winning_team_id = tr.winning_team_id, losing_team_id = tr.losing_team_id
from tournament_slots_results as slots
left join tournament_seeds as sts on sts.seed = slots.strongseed and slots.season = sts.season
left join tournament_slots_results as qual_slot on qual_slot.slot = slots.weakseed and slots.season = qual_slot.season
left join tournament_results as tr on 
(
tr.losing_team_id = sts.team_id
and tr.winning_team_id = qual_slot.winning_team_id
and qual_slot.season = tr.season 
and sts.season = tr.season
) 
or 
(
sts.team_id = tr.winning_team_id 
and qual_slot.winning_team_id = tr.losing_team_id 
and sts.season = tr.season 
and qual_slot.season = tr.season
)
where res.season = slots.season and res.slot = slots.slot and res.winning_team_id IS NULL;

-- This following loops finds the winners of each game
DO
$do$
BEGIN
FOR i IN 1..8 LOOP

update tournament_slots_results res set winning_team_id = tr.winning_team_id, losing_team_id = tr.losing_team_id
from tournament_slots_results as tsr
join tournament_slots_results as sts on tsr.strongseed = sts.slot and sts.season = tsr.season
join tournament_slots_results as wts on tsr.weakseed = wts.slot and wts.season = tsr.season
left join tournament_results as tr on 
(
tr.winning_team_id = sts.winning_team_id
and tr.losing_team_id = wts.winning_team_id
and sts.season = tr.season 
and wts.season = tr.season
) 
or 
(
wts.winning_team_id = tr.winning_team_id 
and sts.winning_team_id = tr.losing_team_id 
and wts.season = tr.season 
and sts.season = tr.season
)
where res.season = tr.season and res.slot = tsr.slot;

END LOOP;
END
$do$

-- select * from tournament_results where season = 'R' and winning_team_id = 637 or losing_team_id = 637;

-- select * from teams where id = 640 or id = 786
-- select * from seasons where season = 'A' or season = 'G'
-- select * from tournament_slots_results where season = 'R' order by slot;
-- select * from tournament_slots_results order by season, slot;
-- select * from tournament_seeds where season = 'R' and seed = 'Z04';
-- select * from teams where id = 662 or id = 625;
-- select * from tournament_seeds where season = 'G'
