--find out DESCRIPTION of crime scene
SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street = "Humphrey Street";

--retrieve interviews TRANSCRIPT from 3 witnesses
SELECT name, transcript FROM interviews
WHERE year = 2021
AND month = 7 AND day = 28
--each witness mentioned 'bakery'
AND transcript LIKE '%bakery%';

--WHO DRIVE AWAY from parking lot: get name and PHONE number through LICENSE PLATE
SELECT name FROM people
--retrieve license plate from security logs between 10:15-10:25
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021
AND month = 7 AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25;

--WHO WITHDRAW money. retrieve names and phone numbers of people with these account numbers
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
--extract account number of the thief
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021
AND month = 7 AND day = 28
AND transaction_type = "withdraw"
AND atm_location = "Leggett Street";

--get the city
SELECT city FROM airports
--find out what the id of the destination airport
JOIN flights ON airports.id = flights.destination_airport_id
WHERE year = 2021
AND month = 7 AND day = 29
--get the earliest flight
ORDER BY hour ASC
LIMIT 1;


--PASSENGERS who took EARLIEST FLIGHT and their phone number and name based on their flight id and passport number
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id in
(SELECT id FROM flights
WHERE year = 2021
AND month = 7 AND day = 29
ORDER BY hour ASC
LIMIT 1)
ORDER BY name;

-- WHO CALLED: get caller
SELECT name FROM people
JOIN phone_calls on people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7
AND day = 28 AND duration < 60;

-- WHOM they CALLED: get receiver
SELECT name FROM people
JOIN phone_calls on people.phone_number = phone_calls.receiver
WHERE year = 2021 AND month = 7
AND day = 28 AND duration < 60;


--get name of accomplice(receiver)
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE caller =
(SELECT phone_number FROM people
WHERE name =
-- get name of the thief: how to get matching values(names) from several tables with INTERSECT
(SELECT name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021 AND month = 7 AND day = 28
AND hour = 10 AND minute BETWEEN 15 AND 25

INTERSECT
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND month = 7 AND day = 28
AND transaction_type = "withdraw" AND atm_location = "Leggett Street"

INTERSECT
SELECT name FROM people
JOIN phone_calls on people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7
AND day = 28 AND duration < 60

INTERSECT
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id in
(SELECT id FROM flights
WHERE year = 2021
AND month = 7 AND day = 29
ORDER BY hour ASC
LIMIT 1)
ORDER BY name)
and year = 2021 and month = 7
and day = 28 and duration < 60);


-- SELECT name FROM people
-- JOIN phone_calls ON people.phone_number = phone_calls.receiver
-- WHERE caller =
-- (SELECT phone_number FROM people
-- WHERE name = 'Bruce')
-- and year = 2021 and month = 7
-- and day = 28 and duration < 60;
