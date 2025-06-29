.PHONY: test test-bills test-amendments test-summaries test-congress test-members test-house-votes test-committees test-committee-reports test-committee-prints test-committee-meetings test-hearings test-congressional-record test-daily-congressional-record test-bound-congressional-record test-house-communication test-house-requirement test-senate-communication test-nomination test-crsreport test-treaty

test:
	python3 -m unittest discover -s tests/ -p "test_*.py" -v

test-bills:
	python3 -m unittest tests/test_bills.py -v

test-amendments:
	python3 -m unittest tests/test_amendments.py -v

test-summaries:
	python3 -m unittest tests/test_summaries.py -v

test-congress:
	python3 -m unittest tests/test_congress.py -v

test-members:
	python3 -m unittest tests/test_members.py -v

test-house-votes:
	python3 -m unittest tests/test_house_votes.py -v

test-committees:
	python3 -m unittest tests/test_committees.py -v

test-committee-reports:
	python3 -m unittest tests/test_committee_reports.py -v

test-committee-prints:
	python3 -m unittest tests/test_committee_prints.py -v

test-committee-meetings:
	python3 -m unittest tests/test_committee_meetings.py -v

test-hearings:
	python3 -m unittest tests/test_hearings.py -v

test-congressional-record:
	python3 -m unittest tests/test_congressional_record.py -v

test-daily-congressional-record:
	python3 -m unittest tests/test_daily_congressional_record.py -v

test-bound-congressional-record:
	python3 -m unittest tests/test_bound_congressional_record.py -v

test-house-communication:
	python3 -m unittest tests/test_house_communication.py -v

test-house-requirement:
	python3 -m unittest tests/test_house_requirement.py -v

test-senate-communication:
	python3 -m unittest tests/test_senate_communication.py -v

test-nomination:
	python3 -m unittest tests/test_nomination.py -v

test-crsreport:
	python3 -m unittest tests/test_crsreport.py -v

test-treaty:
	python3 -m unittest tests/test_treaty.py -v
