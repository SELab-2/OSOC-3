from sqlalchemy.orm import Session

from src.database.models import *
from src.database.enums import *
from src.app.logic.security import get_password_hash

def fill_database(db: Session):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition(year = 2022)
    db.add(edition)
    db.commit()

    # Users
    admin: User = User(name="admin", email="admin@ngmail.com", admin=True)
    coach1: User = User(name="coach1", email="coach1@noutlook.be")
    coach2: User = User(name="coach2", email="coach2@noutlook.be")
    request: User = User(name="request", email="request@ngmail.com")
    db.add(admin)
    db.add(coach1)
    db.add(coach2)
    db.add(request)
    db.commit()
  
    # AuthEmail
    pw_hash = get_password_hash("wachtwoord")
    auth_email_admin: AuthEmail = AuthEmail(user=admin, pw_hash=pw_hash) 
    auth_email_coach1: AuthEmail = AuthEmail(user=coach1, pw_hash=pw_hash) 
    auth_email_coach2: AuthEmail = AuthEmail(user=coach2, pw_hash=pw_hash) 
    auth_email_request: AuthEmail = AuthEmail(user=request, pw_hash=pw_hash) 
    db.add(auth_email_admin)
    db.add(auth_email_coach1)
    db.add(auth_email_coach2)
    db.add(auth_email_request)
    db.commit()

    #Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske", email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True, wants_to_be_student_coach=True, edition=edition)
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",email_address="isabella.christensen@example.com", phone_number="98389723", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student03: Student = Student(first_name="Lotte", last_name="Buss", preferred_name="Lotte",email_address="lotte.buss@example.com", phone_number="0284-0749932", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student04: Student = Student(first_name="Délano", last_name="Van Lienden", preferred_name="Délano",email_address="delano.vanlienden@example.com", phone_number="(128)-049-9143", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student05: Student = Student(first_name="Einar", last_name="Rossebø", preferred_name="Einar",email_address="einar.rossebo@example.com", phone_number="61491822", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student06: Student = Student(first_name="Dave", last_name="Johnston", preferred_name="Dave",email_address="dave.johnston@example.com", phone_number="031-156-2869", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student07: Student = Student(first_name="Fernando", last_name="Stone", preferred_name="Fernando",email_address="fernando.stone@example.com", phone_number="(441)-156-4776", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student08: Student = Student(first_name="Isabelle", last_name="Singh", preferred_name="Isabelle",email_address="isabelle.singh@example.com", phone_number="(338)-531-9957", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student09: Student = Student(first_name="Blake", last_name="Martin", preferred_name="Blake",email_address="blake.martin@example.com", phone_number="404-060-5843", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student10: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student11: Student = Student(first_name="Mehmet", last_name="Balcı", preferred_name="Mehmet",email_address="mehmet.balci@example.com", phone_number="(496)-221-8222", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student12: Student = Student(first_name="Óscar", last_name="das Neves", preferred_name="Óscar",email_address="oscar.dasneves@example.com", phone_number="(47) 6646-0730", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student13: Student = Student(first_name="Melike", last_name="Süleymanoğlu", preferred_name="Melike",email_address="melike.suleymanoglu@example.com", phone_number="(274)-545-3055", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student14: Student = Student(first_name="Magnus", last_name="Schanke", preferred_name="Magnus",email_address="magnus.schanke@example.com", phone_number="63507430", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student15: Student = Student(first_name="Tara", last_name="Howell", preferred_name="Tara",email_address="tara.howell@example.com", phone_number="07-9111-0958", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student16: Student = Student(first_name="Hanni", last_name="Ewers", preferred_name="Hanni",email_address="hanni.ewers@example.com", phone_number="0241-5176890", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student17: Student = Student(first_name="آیناز", last_name="کریمی", preferred_name="آیناز",email_address="aynz.khrymy@example.com", phone_number="009-26345191", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student18: Student = Student(first_name="Vicente", last_name="Garrido", preferred_name="Vicente",email_address="vicente.garrido@example.com", phone_number="987-381-670", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student19: Student = Student(first_name="Elmer", last_name="Morris", preferred_name="Elmer",email_address="elmer.morris@example.com", phone_number="(611)-832-8108", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student20: Student = Student(first_name="Alexis", last_name="Roy", preferred_name="Alexis",email_address="alexis.roy@example.com", phone_number="566-546-7642", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student21: Student = Student(first_name="Lillie", last_name="Kelly", preferred_name="Lillie",email_address="lillie.kelly@example.com", phone_number="(983)-560-1392", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student22: Student = Student(first_name="Karola", last_name="Andersen", preferred_name="Karola",email_address="karola.andersen@example.com", phone_number="0393-3219328", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student23: Student = Student(first_name="Elvine", last_name="Andvik", preferred_name="Elvine",email_address="elvine.andvik@example.com", phone_number="30454610", almuni=True, wants_to_be_student_coach=True, edition=edition)
    student24: Student = Student(first_name="Chris", last_name="Kelly", preferred_name="Chris",email_address="chris.kelly@example.com", phone_number="061-399-0053", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student25: Student = Student(first_name="Aada", last_name="Pollari", preferred_name="Aada",email_address="aada.pollari@example.com", phone_number="02-908-609", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student26: Student = Student(first_name="Sofia", last_name="Haataja", preferred_name="Sofia",email_address="sofia.haataja@example.com", phone_number="06-373-889", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student27: Student = Student(first_name="Charlene", last_name="Gregory", preferred_name="Charlene",email_address="charlene.gregory@example.com", phone_number="(991)-378-7095", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student28: Student = Student(first_name="Danielle", last_name="Chavez", preferred_name="Danielle",email_address="danielle.chavez@example.com", phone_number="01435 91142", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student29: Student = Student(first_name="Nikolaj", last_name="Poulsen", preferred_name="Nikolaj",email_address="nikolaj.poulsen@example.com", phone_number="20525141", almuni=False, wants_to_be_student_coach=False, edition=edition)
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",email_address="marta.marquez@example.com", phone_number="967-895-285", almuni=True, wants_to_be_student_coach=False, edition=edition)
    student31: Student = Student(first_name="Gül", last_name="Barbarosoğlu", preferred_name="Gül",email_address="gul.barbarosoglu@example.com", phone_number="(008)-316-3264", almuni=True, wants_to_be_student_coach=False, edition=edition)
    
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
    db.commit

    #DecisionEmail #TODO: studenten aanmaken

    # InviteLink
    inviteLink1: InviteLink = InviteLink(target_email="newuser1@email.com", edition=edition)
    inviteLink2: InviteLink = InviteLink(target_email="newuser2@email.com", edition=edition)
    db.add(inviteLink1)
    db.add(inviteLink2)
    db.commit()

    # Partner
    partner1: Partner = Partner(name="Partner1")
    partner2: Partner = Partner(name="Partner2")
    partner3: Partner = Partner(name="Partner3")
    db.add(partner1)
    db.add(partner2)
    db.add(partner3)
    db.commit()

    #Project
    #project1: Project = Project(name="project1", 3, )