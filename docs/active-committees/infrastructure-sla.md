# Infrastructure SLA

!!! note "Source"
    Mirrored from [Infrastructure SLA](https://dallasmakerspace.org/wiki/Infrastructure_SLA) on the Dallas Makerspace wiki (CC BY-SA 3.0).

**Committees are voluntary groups, formed by members in order to achieve certain goals.**
To join this committee, contact the committee chairperson. See [Rules and Policies#Committees](../dms-official/rules-and-policies.md#committees) for more information.

### Charter

*Charter approved by BoD 2019-09-08*

#### Purpose

The Infrastructure Group performs operations and maintenance of Dallas Makerspace mechanical/electrical/plumbing (MEP), communications, online presence, and physical security.

#### Infrastructure Officer General Charter

The Infrastructure Officer shall be bound by the [General Officer Charter](../officers/officers.md#general-officer-charter).

#### Governance

The Infrastructure Group is headed by the Technology Officer, who may appoint or dismiss members without cause. The Technology Officer shall record and publically post the names of all members of the Infrastructure Group, noting changes in a timely fashion. The Infrastructure Group shall meet on an as-needed basis and report to the Board when requested by the Board.

#### Operations

The Technology Officer may delegate functions of the Office of the Technology Officer to member(s) of the Infrastructure Group as they deem necessary.

#### Responsibilities of the Office of the Technology Officer

1.  Facility MEP (Mechanical, Electrical, Plumbing)
    1.  Plumbing
    2.  HVAC
    3.  Electrical
    4.  Compressed air
2.  Onsite Electronic Communications / information assets
    1.  LAN
    2.  Wi-fi
    3.  Internet
    4.  Onsite servers
    5.  Phones
    6.  DMS-owned computers
3.  Online presence
    1.  Website (infrastructure)
    2.  Cloud infrastructure
    3.  Internet access
4.  Physical security
    1.  Access control
    2.  Cameras
5.  Contracts related to Infrastructure

#### Finances

The Infrastructure Group shall have a monthly allocation specified by the Board of Directors. This shall be charged against the general fund; Infrastructure Group will retain no balance.

### Policies

The Jump server hosts several virtual machines; including a Windows Server that hosts our VCarve, FeatureCAM, and AutoDesk Inventor software.

- [This link](../systems-and-infrastructure/storing-computer-files.md) provides information about storing and accessing computer files at DMS.
- [Jump Server login](../systems-and-infrastructure/jumpserverlogin.md) (and creating AD account)
- [Jump Server FAQ](../systems-and-infrastructure/jumpserverfaq.md).

### Telephone System

The phone system is a Voice over IP PBX, which consists of a virtual machine running Asterisk 11 with IncredibleGUI 12 on Ubuntu 14.04LTS. We use Google Voice for trunks, providing free calls to anywhere in the US or Canada. Our main number is 214-699-6537.

[VoIP Server Information Page](../voipserver/voipserver.md)

### BoD Annual Election Procedures

Our Bylaws require an annual election of our BoD, the page in the link below details the procedures that were used in the most recent election. These procedures should be updated whenever a change is made.

[BoD Annual Election Procedures](../dallas-makerspace/board-of-directors-annual-election-procedures.md)

### Infrastructure

[Infrastructure](../infrastructure/infrastructure.md)

### Governance Model

Group

### Contact

Post to the Infrastructure category on the [forums](https://talk.dallasmakerspace.org/c/infrastructure), chat with us on [Discord](https://chat.dallasmakerspace.org/), or send an email to <infrastructure@dallasmakerspace.org> (or infra@dallasmakerspace.org) and it will be forwarded to all members of the committee.

### Members

- Andrew Spencer - Infrastructure Officer / CTO (@jast)
- Freddy Calvert
- Tails Hartnett (@hon1nbo ; cybersecurity stickler)
- [Dwight Spencer (DevOps, IT, PM)](https://dallasmakerspace.org/wiki/User:Denzuko)
- [Lisa Selk](https://dallasmakerspace.org/wiki/User:Selk68)
- Andrew LeCody
- Alex Rhodes
- [Bill Gee](https://dallasmakerspace.org/wiki/User:Bill) (@Bill)
- Robert Davidson
- Frank Lima
- Joe Helmstetter
- Jason Ottwell
- Mike Kelp (Code Wizard)
- [john a. gorman (Senior IT Specialist)](https://dallasmakerspace.org/wiki/User:Talkers)
- Stephenie Webb
- James Blocker
- [Justin Edwards](https://dallasmakerspace.org/wiki/User:Ke5bud)
- James Braye
- [Woody](https://dallasmakerspace.org/wiki/User:Woody) (@woody)
- Kyle Crothers

### Moderators

The Infrastructure Committee sponsors a team (Moderator Team) to moderate the Talk Forum with a published set of [moderator guidelines](../infrastructure/moderator-guidelines.md). The Moderator Team desires and promotes an open, transparent environment on Talk that promotes inclusion, diversity of opinions, knowledge sharing, fairness and respect while respecting privacy of all individuals.

### Meeting Minutes

The committee routinely meets on the second Wednesday of every month. Meetings will be posted on [the calendar](https://calendar.dallasmakerspace.org/).

- [Infrastructure Committee Meeting (template)](../infrastructure-meetings/infrastructure-committee-meeting-template.md)

#### 2018

- [Infrastructure Committee Meeting 20180420](../april-meetings/infrastructure-committee-meeting-20180420.md)

### How To Join

1.  Send an email to infrastructure@dallasmakerspace.org and request to join the Infrastructure committee.
2.  Add your name to the list of members on this page.

All pages related to the [Infrastructure Committee](https://dallasmakerspace.org/wiki/Infrastructure_Committee).

## Service Level Agreement - Contents

A Service Level Agreement typically contains the following information (actual contents may vary depending on the type of service):

    The Service Level Agreement contains the contractually relevant data for an IT Service:

- Name of the IT Service
- Clearance information (with location and date)
  - Service Level Manager
  - Client representative
- Contact persons
  - Name of the Service Provider
  - Name of the Service recipient
  - Contact partners/ persons in charge (on client-side as well as on the side of the IT Organization) for
    - Contractual changes
    - Complaints and suggestions
    - Escalations in the case of contractual infringements
    - Service reviews
    - Emergencies
- Contract duration
  - Contract start
  - Contract end
  - Rules for changes to the SLA
    - How are requests for change submitted (deletions, additions or changes to components of the SLA)?
    - How are the requests for change and their implementation controlled?
    - Who is responsible for the clearance of the changes?
  - Rules for termination of the SLA
- Service description
  - Short description of Service
  - Users of the IT Service on the client-side
  - Breakdown of the offered Service into Service groups, e.g. along infrastructure components or IT applications
  - For each Service group:
    - Which Services are offered, e.g.
      - Handling of Service interruptions (by telephone, by remote access, on site?)
      - User Services (user administration, installation, …)
    - What quality is required of the offered Services, e.g.
      - Service times
      - Availability requirements
        - Number of interruptions allowed
        - Availability thresholds (xx,xx %)
        - Downtimes for maintenance (number of allowed downtimes, pre-notification periods)
        - Procedure for announcing interruptions to the Service (planned/ unplanned)
      - Performance requirements
        - Required capacity (lower/upper limit) for the Service
        - Allowed workload/ usage of the Service
        - Response times from applications
        - Reaction and resolution times (according to priorities, definition of priorities e.g. for the classification of Incidents)
      - Requirements for the maintenance of the Service in the event of a disaster
- Relations to other IT Services
- Procedures for requesting the IT Service
  - Requests possible by telephone/fax/mail, ... (addresses, telephone numbers, etc.)
- Responsibilities
  - Of the client (also within the field of IT Security)
  - Responsibilities and liability of the IT Organization
- Quality assurance and Service Level Reporting
  - Measurement procedures
    - Which indicators
    - With which measurement procedures
    - At which intervals
    - Collated into which reports
  - SLA Reviews
    - Intervals at which SLA reviews are to be held
- Service accounting
  - Costs for the provision of the Service
  - Accounting method for the Service
  - Intervals for invoicing
- Glossary
