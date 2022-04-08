from datetime import date
from sqlalchemy.orm import Session

from src.database.models import (User, AuthEmail, Skill, Student,
                                Edition, CoachRequest, DecisionEmail, InviteLink, Partner,
                                Project, ProjectRole, Suggestion)
from src.database.enums import DecisionEnum
from src.app.logic.security import get_password_hash


def fill_database(db: Session):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition = Edition(year=2022, name="ed2022")
    db.add(edition)
    db.commit()

    # Users
    admin: User = User(name="admin", admin=True)
    coach1: User = User(name="coach1")
    coach2: User = User(name="coach2")
    request: User = User(name="request")
    db.add(admin)
    db.add(coach1)
    db.add(coach2)
    db.add(request)
    db.commit()

    # AuthEmail
    pw_hash = get_password_hash("wachtwoord")
    auth_email_admin: AuthEmail = AuthEmail(user=admin, email="admin@ngmail.com", pw_hash=pw_hash)
    auth_email_coach1: AuthEmail = AuthEmail(user=coach1, email="coach1@noutlook.be", pw_hash=pw_hash)
    auth_email_coach2: AuthEmail = AuthEmail(user=coach2, email="coach2@noutlook.be", pw_hash=pw_hash)
    auth_email_request: AuthEmail = AuthEmail(user=request, email="request@ngmail.com", pw_hash=pw_hash)
    db.add(auth_email_admin)
    db.add(auth_email_coach1)
    db.add(auth_email_coach2)
    db.add(auth_email_request)
    db.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    db.add(skill1)
    db.add(skill2)
    db.add(skill3)
    db.add(skill4)
    db.add(skill5)
    db.add(skill6)
    db.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",
                                 email_address="isabella.christensen@example.com", phone_number="98389723", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student03: Student = Student(first_name="Lotte", last_name="Buss", preferred_name="Lotte",
                                 email_address="lotte.buss@example.com", phone_number="0284-0749932", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student04: Student = Student(first_name="Délano", last_name="Van Lienden", preferred_name="Délano",
                                 email_address="delano.vanlienden@mail.com", phone_number="128-049-9143", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student05: Student = Student(first_name="Einar", last_name="Rossebø", preferred_name="Einar",
                                 email_address="einar.rossebo@example.com", phone_number="61491822", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student06: Student = Student(first_name="Dave", last_name="Johnston", preferred_name="Dave",
                                 email_address="dave.johnston@example.com", phone_number="031-156-2869", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student07: Student = Student(first_name="Fernando", last_name="Stone", preferred_name="Fernando",
                                 email_address="fernando.stone@mail.com", phone_number="(441)-156-4776", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student08: Student = Student(first_name="Isabelle", last_name="Singh", preferred_name="Isabelle",
                                 email_address="isabelle.singh@example.com", phone_number="(338)-531-9957", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student09: Student = Student(first_name="Blake", last_name="Martin", preferred_name="Blake",
                                 email_address="blake.martin@example.com", phone_number="404-060-5843", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student10: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",
                                 email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2])
    student11: Student = Student(first_name="Mehmet", last_name="Balci", preferred_name="Mehmet",
                                 email_address="mehmet.balci@example.com", phone_number="(496)-221-8222", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student12: Student = Student(first_name="Óscar", last_name="das Neves", preferred_name="Óscar",
                                 email_address="oscar.dasneves@example.com", phone_number="(47) 6646-0730", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill4])
    student13: Student = Student(first_name="Melike", last_name="Süleymanoğlu", preferred_name="Melike",
                                 email_address="melike.suleymanoglu@mail.com", phone_number="274-545-3055", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student14: Student = Student(first_name="Magnus", last_name="Schanke", preferred_name="Magnus",
                                 email_address="magnus.schanke@example.com", phone_number="63507430", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student15: Student = Student(first_name="Tara", last_name="Howell", preferred_name="Tara",
                                 email_address="tara.howell@example.com", phone_number="07-9111-0958", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student16: Student = Student(first_name="Hanni", last_name="Ewers", preferred_name="Hanni",
                                 email_address="hanni.ewers@example.com", phone_number="0241-5176890", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill1, skill6, skill5])
    student17: Student = Student(first_name="آیناز", last_name="کریمی", preferred_name="آیناز",
                                 email_address="aynz.khrymy@example.com", phone_number="009-26345191", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student18: Student = Student(first_name="Vicente", last_name="Garrido", preferred_name="Vicente",
                                 email_address="vicente.garrido@example.com", phone_number="987-381-670", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student19: Student = Student(first_name="Elmer", last_name="Morris", preferred_name="Elmer",
                                 email_address="elmer.morris@example.com", phone_number="(611)-832-8108", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student20: Student = Student(first_name="Alexis", last_name="Roy", preferred_name="Alexis",
                                 email_address="alexis.roy@example.com", phone_number="566-546-7642", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student21: Student = Student(first_name="Lillie", last_name="Kelly", preferred_name="Lillie",
                                 email_address="lillie.kelly@example.com", phone_number="(983)-560-1392", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student22: Student = Student(first_name="Karola", last_name="Andersen", preferred_name="Karola",
                                 email_address="karola.andersen@example.com", phone_number="0393-3219328", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student23: Student = Student(first_name="Elvine", last_name="Andvik", preferred_name="Elvine",
                                 email_address="elvine.andvik@example.com", phone_number="30454610", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4, skill5])
    student24: Student = Student(first_name="Chris", last_name="Kelly", preferred_name="Chris",
                                 email_address="chris.kelly@example.com", phone_number="061-399-0053", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill4])
    student25: Student = Student(first_name="Aada", last_name="Pollari", preferred_name="Aada",
                                 email_address="aada.pollari@example.com", phone_number="02-908-609", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student26: Student = Student(first_name="Sofia", last_name="Haataja", preferred_name="Sofia",
                                 email_address="sofia.haataja@example.com", phone_number="06-373-889", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student27: Student = Student(first_name="Charlene", last_name="Gregory", preferred_name="Charlene",
                                 email_address="charlene.gregory@mail.com", phone_number="(991)-378-7095", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student28: Student = Student(first_name="Danielle", last_name="Chavez", preferred_name="Danielle",
                                 email_address="danielle.chavez@example.com", phone_number="01435 91142", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student29: Student = Student(first_name="Nikolaj", last_name="Poulsen", preferred_name="Nikolaj",
                                 email_address="nikolaj.poulsen@example.com", phone_number="20525141", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])
    student31: Student = Student(first_name="Gül", last_name="Barbarosoğlu", preferred_name="Gül",
                                 email_address="gul.barbarosoglu@mail.com", phone_number="(008)-316-3264", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    db.add(student01)
    db.add(student02)
    db.add(student03)
    db.add(student04)
    db.add(student05)
    db.add(student06)
    db.add(student07)
    db.add(student08)
    db.add(student09)
    db.add(student10)
    db.add(student11)
    db.add(student12)
    db.add(student13)
    db.add(student14)
    db.add(student15)
    db.add(student16)
    db.add(student17)
    db.add(student18)
    db.add(student19)
    db.add(student20)
    db.add(student21)
    db.add(student22)
    db.add(student23)
    db.add(student24)
    db.add(student25)
    db.add(student26)
    db.add(student27)
    db.add(student28)
    db.add(student29)
    db.add(student30)
    db.add(student31)
    db.commit()

    # CoachRequest
    coach_request: CoachRequest = CoachRequest(edition=edition, user=request)
    db.add(coach_request)
    db.commit()

    # DecisionEmail
    decision_email1: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.NO, student=student29, date=date.today())
    decision_email2: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.YES, student=student09, date=date.today())
    decision_email3: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.YES, student=student10, date=date.today())
    decision_email4: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.YES, student=student11, date=date.today())
    decision_email5: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.YES, student=student12, date=date.today())
    decision_email6: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.MAYBE, student=student06, date=date.today())
    decision_email7: DecisionEmail = DecisionEmail(
        decision=DecisionEnum.MAYBE, student=student26, date=date.today())
    db.add(decision_email1)
    db.add(decision_email2)
    db.add(decision_email3)
    db.add(decision_email4)
    db.add(decision_email5)
    db.add(decision_email6)
    db.add(decision_email7)
    db.commit()

    # InviteLink
    invite_link1: InviteLink = InviteLink(
        target_email="newuser1@email.com", edition=edition)
    invite_link2: InviteLink = InviteLink(
        target_email="newuser2@email.com", edition=edition)
    db.add(invite_link1)
    db.add(invite_link2)
    db.commit()

    # Partner
    partner1: Partner = Partner(name="Partner1")
    partner2: Partner = Partner(name="Partner2")
    partner3: Partner = Partner(name="Partner3")
    db.add(partner1)
    db.add(partner2)
    db.add(partner3)
    db.commit()

    # Project
    project1: Project = Project(
        name="project1", number_of_students=3, edition=edition, partners=[partner1])
    project2: Project = Project(
        name="project2", number_of_students=6, edition=edition, partners=[partner2])
    project3: Project = Project(
        name="project3", number_of_students=2, edition=edition, partners=[partner3])
    project4: Project = Project(
        name="project4", number_of_students=9, edition=edition, partners=[partner1, partner3])
    db.add(project1)
    db.add(project2)
    db.add(project3)
    db.add(project4)
    db.commit()

    # Suggestion
    suggestion1: Suggestion = Suggestion(
        student=student01, coach=coach1, argumentation="Good student", suggestion=DecisionEnum.YES)
    suggestion2: Suggestion = Suggestion(
        student=student01, coach=coach2, argumentation="Good student", suggestion=DecisionEnum.YES)
    suggestion3: Suggestion = Suggestion(
        student=student12, coach=coach1, argumentation="Not a good student", suggestion=DecisionEnum.NO)
    suggestion4: Suggestion = Suggestion(
        student=student03, coach=coach2, argumentation="Maybe a student", suggestion=DecisionEnum.MAYBE)
    suggestion5: Suggestion = Suggestion(
        student=student04, coach=coach1, argumentation="Not a good student", suggestion=DecisionEnum.NO)
    suggestion6: Suggestion = Suggestion(
        student=student13, coach=coach1, argumentation="Good student", suggestion=DecisionEnum.YES)
    suggestion7: Suggestion = Suggestion(
        student=student01, coach=admin, argumentation="Not a good student", suggestion=DecisionEnum.NO)
    suggestion8: Suggestion = Suggestion(
        student=student12, coach=admin, argumentation="Good student", suggestion=DecisionEnum.YES)
    db.add(suggestion1)
    db.add(suggestion2)
    db.add(suggestion3)
    db.add(suggestion4)
    db.add(suggestion5)
    db.add(suggestion6)
    db.add(suggestion7)
    db.add(suggestion8)
    db.commit()

    # ProjectRole
    project_role1: ProjectRole = ProjectRole(
        student=student01, project=project1, skill=skill1, drafter=coach1, argumentation="argmunet")
    project_role2: ProjectRole = ProjectRole(  # This brings a confict
        student=student01, project=project2, skill=skill2, drafter=coach2, argumentation="argmunet")
    project_role3: ProjectRole = ProjectRole(
        student=student09, project=project2, skill=skill3, drafter=coach1, argumentation="argmunet")
    project_role3: ProjectRole = ProjectRole(
        student=student05, project=project1, skill=skill4, drafter=coach1, argumentation="argmunet")
    project_role4: ProjectRole = ProjectRole(
        student=student25, project=project3, skill=skill5, drafter=coach1, argumentation="argmunet")
    project_role5: ProjectRole = ProjectRole(
        student=student29, project=project3, skill=skill6, drafter=coach1, argumentation="argmunet")
    project_role6: ProjectRole = ProjectRole(
        student=student03, project=project4, skill=skill5, drafter=coach1, argumentation="argmunet")
    project_role7: ProjectRole = ProjectRole(
        student=student13, project=project4, skill=skill4, drafter=coach1, argumentation="argmunet")
    db.add(project_role1)
    db.add(project_role2)
    db.add(project_role3)
    db.add(project_role4)
    db.add(project_role5)
    db.add(project_role6)
    db.add(project_role7)
    db.commit()
