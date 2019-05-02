(*
Tung Phan
California Institute of Technology
TLA+ Specifications for an Automated Valet Parking Garage
May 02, 2019
*)
-------------------------- MODULE ProvableTimeParking -------------------------
EXTENDS Integers, Sequences, FiniteSets

CONSTANT
    V,  (* total number of valets *)
    P,  (* total number of parking spaces *)
    PARK_TIME,  (* time taken to park a car *)
    RETURN_TIME,  (* time taken to return a car *)
    MAX_WAIT,  (* each car waits no longer than this amount *)
    TIC_TOC (* smallest possible clock increment *)
  
ASSUME
    /\ P \in Int
    /\ PARK_TIME \in Int
    /\ RETURN_TIME \in Int
    /\ MAX_WAIT \in Int
    /\ TIC_TOC \in Int
    /\ V \in Int

VARIABLES
    garage_state, 
    wait_line,
    valet_state

 vars == <<garage_state, wait_line, valet_state>>
(***************************************************************************)
(* Some useful sets and operators.                                         *)
(***************************************************************************)
Status == {"idle", "empty", "parking", "parked", "requested", "returning"}
Spaces == 1..P
Valets == 1..V
RECURSIVE Sum(_,_)
Sum(f,S) == IF S = {} THEN 0
		      ELSE LET x  == CHOOSE x \in S: TRUE
		      	   IN f[x] + Sum(f, S \ {x})
SumFunc(f) == Sum(f, DOMAIN f)
FilterInUse(f) == [x \in Spaces |-> IF f[x][1] \in {"parked", "requested", "parking"}
                                   THEN 1 ELSE 0]
NumParked == SumFunc(FilterInUse(garage_state))
NumWaiting == Len(wait_line)

ArgMax(f) == CHOOSE x \in DOMAIN f: \A y \in DOMAIN f: f[x] >= f[y]
RequestSet == {x \in Spaces: garage_state[x][1] = "requested"}
GetRequestTimers == [x \in RequestSet |-> garage_state[x][2]]
RequestLongest == ArgMax(GetRequestTimers)
WaitLineLongestTime == IF wait_line = << >>
 	               THEN -1
	               ELSE Head(wait_line)
Max(x,y) == IF x >= y
            THEN x
	    ELSE y

Min(x,y) == IF x < y
            THEN x
	    ELSE y
	    
LongestWait == IF RequestSet = {}
               THEN WaitLineLongestTime
	       ELSE Max(garage_state[RequestLongest][2], WaitLineLongestTime)

ReturnPriority == /\ RequestSet /= {}
		  /\ \/ wait_line = << >> 
    		     \/ garage_state[RequestLongest][2] >= WaitLineLongestTime

ParkPriority == ~ReturnPriority

IsEmpty(x) == garage_state[x][1] \in {"empty"}
IsOccupied(x) == garage_state[x][1] \in {"parked"}
MakeEmpty(x) == garage_state' = [garage_state EXCEPT ![x] = <<"empty", -1>>]
BusyNum == Cardinality({x \in Valets: valet_state[x][1] /= "idle"})
AllValetsBusy == BusyNum = V 
OperateAtFullCapacity == \/ AllValetsBusy
			 \/ BusyNum = P

ReturnOK == \E x \in Valets: /\ valet_state[x][1] = "returning"
			     /\ valet_state[x][2] = RETURN_TIME
ParkOK == \E x \in Valets:   /\ valet_state[x][1] = "parking"
			     /\ valet_state[x][2] = PARK_TIME
(***************************************************************************)
(* Specifications.                                                         *)
(***************************************************************************)
TypeInvariant ==
    /\ garage_state \in [Spaces -> Status \times Int]
    /\ valet_state \in [Valets -> Status \times Int \times (Spaces \union {0})]
    /\ wait_line \in [1..NumWaiting -> Int]
    /\ DOMAIN garage_state = Spaces
    /\ DOMAIN valet_state = Valets

Init ==
    /\ garage_state = [x \in Spaces |-> <<"empty", -1>>]
    /\ wait_line = << >>
    /\ valet_state = [x \in Valets |-> <<"idle", -1, 0 >>]

AdvanceTime(dt) == /\  garage_state' = [x \in Spaces |-> IF
		   				            garage_state[x][1] \in
							    {"requested"}
							    THEN
							    [garage_state[x]
							    EXCEPT ![2] = @+dt]
							    ELSE 
							      garage_state[x]]
                   /\ wait_line' = [s \in 1..NumWaiting |-> wait_line[s] + dt]
		   /\ valet_state' = [x \in Valets |-> IF 
							   valet_state[x][1]
							   \notin
							   {"idle"}
							   THEN
							   [valet_state[x] 
							   EXCEPT ![2] = @+dt]
							   ELSE
							   valet_state[x]]
NewCar ==
    /\ NumWaiting + NumParked < P
    /\ wait_line' = Append(wait_line, 0)
    /\ UNCHANGED <<garage_state, valet_state>>

BeginParkCar ==
    /\ ~AllValetsBusy
    /\ NumWaiting > 0
    /\ \E x \in Spaces: IsEmpty(x)
    /\ wait_line' = Tail(wait_line)
    /\ LET dest == CHOOSE x \in Spaces: IsEmpty(x)
       IN 
          /\ garage_state' = [garage_state EXCEPT ![dest][1] = "parking"]
          /\ LET v == CHOOSE x \in Valets: valet_state[x][1] = "idle"
              IN  valet_state' = [valet_state EXCEPT ![v] = <<"parking", 0, dest>>]

DoneParkCar ==
    /\ \E s \in Valets: /\ valet_state[s][1] = "parking"
			/\ valet_state[s][2] = PARK_TIME
    /\ LET fin == CHOOSE s \in Valets: /\ valet_state[s][1] = "parking"
          			       /\ valet_state[s][2] = PARK_TIME
       IN /\ garage_state' = [garage_state EXCEPT ![valet_state[fin][3]] = <<"parked", -1>>]
	  /\ valet_state'  = [valet_state EXCEPT ![fin] = <<"idle", -1, 0>>]
    /\ UNCHANGED <<wait_line>>

BeginReturnCar ==
    /\ ~AllValetsBusy
    /\ RequestSet /= {} 
    /\ LET req == RequestLongest
       IN /\ MakeEmpty(req)
          /\ LET v == CHOOSE x \in Valets: valet_state[x][1] \in {"idle"}
             IN  valet_state' = [valet_state EXCEPT ![v] = <<"returning", 0, req>>]
    /\ UNCHANGED <<wait_line>>

DoneReturnCar ==  /\ \E s \in Valets: /\ valet_state[s][1] = "returning"
		                      /\ valet_state[s][2] = RETURN_TIME
		  /\  LET fin == CHOOSE s \in Valets: /\ valet_state[s][1] = "returning"
    						      /\ valet_state[s][2] = RETURN_TIME
                      IN valet_state'  = [valet_state EXCEPT ![fin] = <<"idle", -1, 0>>]
                  /\ UNCHANGED <<wait_line, garage_state>>

ReturnRequest == /\ \E s \in Spaces: garage_state[s][1] = "parked"
		 /\ LET t == CHOOSE s \in Spaces: garage_state[s][1] = "parked"
   		    IN garage_state' = [garage_state EXCEPT ![t] = <<"requested",
		    0>>]
                 /\ UNCHANGED <<wait_line, valet_state>>
Next == 
        \/ /\ OperateAtFullCapacity
           /\ ~ReturnOK
	   /\ ~ParkOK
           /\ AdvanceTime(TIC_TOC)
        \/ /\ ReturnOK 	   
	   /\ DoneReturnCar
        \/ /\ ParkOK 
	   /\ DoneParkCar
        \/ NewCar
 	\/ /\ ReturnPriority
           /\ BeginReturnCar
	\/ /\ ParkPriority
           /\ BeginParkCar
        \/ ReturnRequest 

Spec == /\ Init
        /\ [][Next]_vars

GoodWaitTimes == LongestWait <= MAX_WAIT
         
Inv == 	/\ TypeInvariant
	/\ GoodWaitTimes
===============================================================================
