Run Instructions:
    python version: 3+
    install requirements: pip3 install -r requirements.txt
    run: python.exe apiData.py

Task 1

Create code can be found in the CreateScript.sql file

Table Design:
vote_share:
RidingNumber is the primary key since it is the only unique identifier. If this needed to be expanded we could use a composite primary key or use another table to store the riding/date/election type/etc 
We don't really cxare about riding name filtering (for now) so it doesn't need an index. TotalVotes and turnout need indexes in cases where we are looking for the election with the highestlowest turnout/number of votes.
Party vote share needs to be in a collective index to make the greatest operation (used to select the winner) less time consuming

candidates
RidingNumber is again the primary key, ultimately, this could just be merged with the vote_share table since it should theorectically be a 1-1 relationship.
Candidate names need to be indexed together since our query for looking for names of candidates will rely on all of the columns being indexed
Candidate name is formated as <first_name> <last_name>

For both tables, using the default btree index is sufficient since it handles the operations that I am trying to use the index for (=, like, etc.)

Other notes on python script:
-could probably be using a connection pool for this task if optimization of runtime was a requirement, however because I don't know the rate limiting on the api in question, it's probably safer not to multi thread. If this was a system designed for expansion we would probably want to use connection pools/context manager for establishing connections (there might also be a better way than that)
-may change the above to actually use it since we need to make ~350 api calls
-depending on the size of the data, you may want to split the tasks up to reduce system memory usage but in this case it's probably fine to keep all the calls together

Task 2
1. 
SELECT COUNT(*), res."ridingWinner" FROM (select vs."RidingNumber", 
    case GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") 
            when vs."ConVoteShare" then 'CON'
            when vs."LibVoteShare" then 'LIB'
            when vs."NDPVoteShare" then 'NDP'
            when vs."GreenVoteShare" then 'GRN'
            when vs."PPCVoteShare" then 'PPC'
            when vs."BQVoteShare" then 'BQ'
            else null
        END "ridingWinner"
    from vote_share vs) res
    group by res."ridingWinner"
order BY COUNT(*) desc limit 1

Answer: Liberals Won with 184 seats

2. 
SELECT vs."RidingNumber", case GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") 
            when vs."ConVoteShare" THEN c."ConCandidate"
            when vs."LibVoteShare" THEN c."LibCandidate"
            when vs."NDPVoteShare" THEN c."NDPCandidate"
            when vs."GreenVoteShare" THEN c."GreenCandidate"
            when vs."PPCVoteShare" THEN c."PPCCandidate"
            when vs."BQVoteShare" THEN c."BQCandidate"
            else null
        END "ridingWinner",
        case GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    		vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") 
            when vs."ConVoteShare" then 'CON'
            when vs."LibVoteShare" then 'LIB'
            when vs."NDPVoteShare" then 'NDP'
            when vs."GreenVoteShare" then 'GRN'
            when vs."PPCVoteShare" then 'PPC'
            when vs."BQVoteShare" then 'BQ'
            else null
        END "winningParty",
        GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    		vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") "voteShare"
    from vote_share vs join candidates c on 
    vs."RidingNumber"=c."RidingNumber" 
    ORDER BY "voteShare" DESC LIMIT 1

Answer: 261, Conservative Party

3.
SELECT * FROM (
 SELECT vs."RidingNumber", case GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") 
            when vs."ConVoteShare" THEN c."ConCandidate"
            when vs."LibVoteShare" THEN c."LibCandidate"
            when vs."NDPVoteShare" THEN c."NDPCandidate"
            when vs."GreenVoteShare" THEN c."GreenCandidate"
            when vs."PPCVoteShare" THEN c."PPCCandidate"
            when vs."BQVoteShare" THEN c."BQCandidate"
            else null
        END "ridingWinner"
    from vote_share vs join candidates c on 
    vs."RidingNumber"=c."RidingNumber" ) a
    WHERE a."ridingWinner" LIKE 'John%'

Answer: 30, 114, 193, 205,281

4. 
SELECT COUNT(*), res."ridingWinner" FROM (select vs."RidingNumber", 
    case GREATEST(vs."ConVoteShare", vs."LibVoteShare",
    vs."NDPVoteShare",vs."GreenVoteShare",vs."PPCVoteShare") 
            when vs."ConVoteShare" then 'CON'
            when vs."LibVoteShare" then 'LIB'
            when vs."NDPVoteShare" then 'NDP'
            when vs."GreenVoteShare" then 'GRN'
            when vs."PPCVoteShare" then 'PPC'
            when vs."BQVoteShare" then 'BQ'
            else null
        END "ridingWinner"
    from vote_share vs) res
    group by res."ridingWinner"
order BY COUNT(*) asc limit 1
Note: no need for having clause here, but in theory we could use it to filter

Answer: 3, Green Party


To be clear, I am not certain I got everything exactly correct/optimized (this was my first time using postgres, previously I have used MySQL and sqlite3 which are usually a little more hands off/lenient), so obviously take my feedback with a grain of salt.
Feedback on Test:
-make it clear what you are looking for: this is a small dataset, so optimization of inserts is not really relevant, but would absolutely be for larger datasets
-allow creativity in table design: giving us the table design (minus indexes) doesn't really allow people to show their sql skill, especially because indexes can often depend on the queries we want to run. Instead I would suggest giving the data we need to model, but allow creativity in the table design and columns. Also judge for column/table names and proper design. Scope is very limited (but that is probably intentional, I do understand that)
-creativity above would also allow for more efficient queries to be used
-Enforce a time limit (forced table design): this could give some insight into initial thought process
-Overall it is a good test for basic python knowledge and contructing custom sql queries on data


Aside - Table design could also be something like (I didn't model this in an ER diagram, so there might be some issues, but this is the general concept):

-candidates
RidingNumber(PK)
CandidateID (FK)
CandidatePartyID (FK)
notes:
each row holds the data needed to get the candidates and which party they represent

-candidateInfo
CandidateID(PK)
FirstName
LastName
CandidateInfo (if needed some notes)
notes:
Can't have party here bc people can run for multiple parties in different elections

-party_info
PartyID(PK)
PartyNameEn
PartyNameFr
PartyShortNameEn
PartyShortNameFr
notes:
index on all of the names individually
splitting this into a new table instead of cols allows us to easily add more parties later one if they start existing/being relevant

-Ridings
RidingNumber (PK)
RidingNameEn
RidingNameFr
AdditionalRidingInfo (if needed)
notes:
index on names individually

-vote_share
RidingNumber (FK)
PartyID
--> these two should be the composite key/effective composite key, if needed later when we do years/diff elections it may split to become part of a fact table
TotalVotes
Turnout
Notes:
index on PartyID
index on TotalVotes
index on Turnout
Individual indexes for sorting and filtering operations

From this starting point, we can more easily expand the dataset to include other elections
Joins can be used to get all of the info about who wins elections/party/candidate, etc along with more specific info


