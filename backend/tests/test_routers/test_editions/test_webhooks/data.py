import random

from faker import Faker
from faker.providers import person

faker: Faker = Faker()
faker.add_provider(person)

faker.name()


def create_webhook_event(
        first_name: str = None,
        last_name: str = None,
        preferred_name: str = None,
        wants_to_be_student_coach: bool = None,
        phone_number: str = None,
        email_address: str = None
) -> dict:
    if not first_name:
        first_name = faker.first_name()
    if not last_name:
        last_name = faker.last_name()
    if not preferred_name:
        preferred_name = faker.first_name()
    if wants_to_be_student_coach is None:
        wants_to_be_student_coach = random.choice([True, False])
    if not phone_number:
        phone_number = faker.phone_number()
    if not email_address:
        email_address = faker.email()

    return {
        "eventId": "5933d05a-b197-45ec-b95c-30c5be43fc80",
        "createdAt": "2022-03-03T10:20:00.859Z",
        "data": {
            "responseId": "85e41402-b5b9-4a24-ac0e-344caa33f985",
            "submissionId": "wkv6d3",
            "respondentId": "63xOJm",
            "formId": "wkjyM3",
            "formName": "#osoc22 student application form",
            "createdAt": "2021-05-12T11:52:57.879Z",
            "fields": [
                {
                    "key": "question_nGRzxz",
                    "label": "Will you live in Belgium in July 2022?*",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                        "444fd1f8-756a-4a24-8189-a306c0fe94b0"
                    ]),
                    "options": [
                        {
                            "id": "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                            "text": "Yes"
                        },
                        {
                            "id": "444fd1f8-756a-4a24-8189-a306c0fe94b0",
                            "text": "No"
                        }
                    ]
                },
                {
                    "key": "question_mO7zDA",
                    "label": "Are you able to work 128 hours with a student employment agreement, or as a volunteer?*",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                        "5b519077-25c5-4d20-ab7f-2da844989ddb",
                        "f7fc01d2-a274-413b-8ea2-c0630d075e03",
                        "398e4fe0-c307-4bce-9120-2079d35fe184"
                    ]),
                    "options": [
                        {
                            "id": "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                            "text": "Yes, I can work with a student employment agreement in Belgium"
                        },
                        {
                            "id": "5b519077-25c5-4d20-ab7f-2da844989ddb",
                            "text": "Yes, I can work as a volunteer in Belgium"
                        },
                        {
                            "id": "f7fc01d2-a274-413b-8ea2-c0630d075e03",
                            "text": "No – but I would like to join this experience for free"
                        },
                        {
                            "id": "398e4fe0-c307-4bce-9120-2079d35fe184",
                            "text": "No, I won’t be able to work as a student, as a volunteer or for free."
                        }
                    ]
                },
                {
                    "key": "question_mVz0Ll",
                    "label": "Can you work during the month of July, Monday through Thursday (~09:00 to 17:00)?*",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                        "748287a7-7b52-4746-8c5f-323caedcbbee",
                    ]),
                    "options": [
                        {
                            "id": "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                            "text": "Yes"
                        },
                        {
                            "id": "748287a7-7b52-4746-8c5f-323caedcbbee",
                            "text": "No, I wouldn't be able to work for the majority of days."
                        }
                    ]
                },
                {
                    "key": "question_nPz6d0",
                    "label": "Are there any responsibilities you might have which could hinder you during the day?",
                    "type": "TEXTAREA",
                    "value": faker.sentence(50)
                },
                {
                    "key": "question_3ExXkL",
                    "label": "Birth name",
                    "type": "INPUT_TEXT",
                    "value": first_name
                },
                {
                    "key": "question_nro6jL",
                    "label": "Last name",
                    "type": "INPUT_TEXT",
                    "value": last_name
                },
                {
                    "key": "question_w4K84o",
                    "label": "Would you like to be called by a different name than your birth name?",
                    "type": "MULTIPLE_CHOICE",
                    "value": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                    "options": [
                        {
                            "id": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                            "text": "Yes"
                        },
                        {
                            "id": "10532c12-72fe-46c1-aca6-54e6185d385d",
                            "text": "No"
                        }
                    ]
                },
                {
                    "key": "question_3jlya9",
                    "label": "How would you like to be called?",
                    "type": "INPUT_TEXT",
                    "value": preferred_name
                },
                {
                    "key": "question_w2KeEb",
                    "label": "What is your gender?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                        "3b3e4851-354d-4135-92e0-7cab57041fc5",
                        "ae4a4c95-4f22-48b9-892e-80d38bbe7ef1",
                        "20ba24a6-b52a-43ae-a517-556b139a8984",
                    ]),
                    "options": [
                        {
                            "id": "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                            "text": "Female"
                        },
                        {
                            "id": "3b3e4851-354d-4135-92e0-7cab57041fc5",
                            "text": "Male"
                        },
                        {
                            "id": "ae4a4c95-4f22-48b9-892e-80d38bbe7ef1",
                            "text": "Transgender"
                        },
                        {
                            "id": "20ba24a6-b52a-43ae-a517-556b139a8984",
                            "text": "Rather not say"
                        }
                    ]
                },
                {
                    "key": "question_3xJpX9",
                    "label": "Would you like to add your pronouns?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "980614af-52d8-45d9-acb6-9d76952a86f1",
                        "ea012b47-896a-4264-b876-35c7e7392a06",
                    ]),
                    "options": [
                        {
                            "id": "980614af-52d8-45d9-acb6-9d76952a86f1",
                            "text": "Yes"
                        },
                        {
                            "id": "ea012b47-896a-4264-b876-35c7e7392a06",
                            "text": "No"
                        }
                    ]
                },
                {
                    "key": "question_mZ2Njv",
                    "label": "Which pronouns do you prefer?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "7719f945-47ca-4166-9aa3-a3a2e1387009",
                        "d9245c04-4abe-488e-a884-17f6c501c1eb",
                        "b78cb089-3e57-484e-bb86-03f3cc753571",
                        "2d74b670-9f74-481a-bd2f-b8b06668f0a4",
                        "a9145194-f930-436e-b0e0-340e7c3fac3e",
                        "e6d5eae6-9340-44ca-a268-934e53ebf707",
                        "ac94baff-9650-4751-83fe-b8315ddedb80",
                    ]),
                    "options": [
                        {
                            "id": "7719f945-47ca-4166-9aa3-a3a2e1387009",
                            "text": "she/her/hers"
                        },
                        {
                            "id": "d9245c04-4abe-488e-a884-17f6c501c1eb",
                            "text": "he/him/his"
                        },
                        {
                            "id": "b78cb089-3e57-484e-bb86-03f3cc753571",
                            "text": "they/them/theirs"
                        },
                        {
                            "id": "2d74b670-9f74-481a-bd2f-b8b06668f0a4",
                            "text": "ze/hir/hir "
                        },
                        {
                            "id": "a9145194-f930-436e-b0e0-340e7c3fac3e",
                            "text": "by firstname"
                        },
                        {
                            "id": "e6d5eae6-9340-44ca-a268-934e53ebf707",
                            "text": "by call name"
                        },
                        {
                            "id": "ac94baff-9650-4751-83fe-b8315ddedb80",
                            "text": "other"
                        }
                    ]
                },
                {
                    "key": "question_3N76pb",
                    "label": "Enter your pronouns",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_3qRd4k",
                    "label": "What language are you most fluent in?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                        "aafb7b8e-e437-440c-a3c6-22a2b61da769",
                        "06efe9b0-8187-4f8c-9f88-53da49177a28",
                        "f4b3f9c9-525e-4bd2-949c-3b52e04477ca",
                    ]),
                    "options": [
                        {
                            "id": "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                            "text": "Dutch"
                        },
                        {
                            "id": "aafb7b8e-e437-440c-a3c6-22a2b61da769",
                            "text": "English"
                        },
                        {
                            "id": "06efe9b0-8187-4f8c-9f88-53da49177a28",
                            "text": "French"
                        },
                        {
                            "id": "f4b3f9c9-525e-4bd2-949c-3b52e04477ca",
                            "text": "German"
                        },
                        {
                            "id": "b6902bde-6134-442d-a8a8-18e882e3e09d",
                            "text": "Other"
                        }
                    ]
                },
                {
                    "key": "question_wQ7DKk",
                    "label": "What language are you most fluent in?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_n97Wq4",
                    "label": "How would you rate your English?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "0288cfa1-a19a-40f4-a172-8b9335152d57",
                        "9de70dc1-c4b6-4734-84d1-3e3a2a29a70f",
                        "a5464911-6714-490b-a370-eb3de514573a",
                        "10ccead0-4539-4695-978b-16a24c1a1fe1",
                        "784e392f-9e56-4bba-8cdd-1a85e3194352",
                    ]),
                    "options": [
                        {
                            "id": "0288cfa1-a19a-40f4-a172-8b9335152d57",
                            "text": "★ I can understand your form, but it is hard for me to reply."
                        },
                        {
                            "id": "9de70dc1-c4b6-4734-84d1-3e3a2a29a70f",
                            "text": "★★ I can have simple conversations."
                        },
                        {
                            "id": "a5464911-6714-490b-a370-eb3de514573a",
                            "text": "★★★ I can express myself, understand people and get a point across."
                        },
                        {
                            "id": "10ccead0-4539-4695-978b-16a24c1a1fe1",
                            "text": "★★★★ I can have extensive and complicated conversations."
                        },
                        {
                            "id": "784e392f-9e56-4bba-8cdd-1a85e3194352",
                            "text": "★★★★★ I am fluent."
                        }
                    ]
                },
                {
                    "key": "question_mea6qo",
                    "label": "Phone number",
                    "type": "INPUT_PHONE_NUMBER",
                    "value": phone_number
                },
                {
                    "key": "question_nW8NOQ",
                    "label": "Your email address\n",
                    "type": "INPUT_EMAIL",
                    "value": email_address
                },
                {
                    "key": "question_wa26Qy",
                    "label": "Upload your CV – size limit 10MB",
                    "type": "FILE_UPLOAD",
                    "value": [
                        {
                            "name": "panel.png",
                            "url": "https://rubye.net/images/panel.png",
                            "mimeType": "image/png",
                            "size": 4033
                        }
                    ]
                },
                {
                    "key": "question_m6Z785",
                    "label": "Or link to your CV",
                    "type": "INPUT_LINK",
                    "value": faker.url()
                },
                {
                    "key": "question_w7NWRz",
                    "label": "Upload your portfolio – size limit 10MB",
                    "type": "FILE_UPLOAD",
                    "value": [
                        {
                            "name": "Tuna.png",
                            "url": "http://eliza.name/images/Tuna.png",
                            "mimeType": "image/png",
                            "size": 43843
                        }
                    ]
                },
                {
                    "key": "question_wbW75E",
                    "label": "Or link to your portfolio / GitHub",
                    "type": "INPUT_LINK",
                    "value": faker.url()
                },
                {
                    "key": "question_wABd7N",
                    "label": "Upload your motivation – size limit 10MB",
                    "type": "FILE_UPLOAD",
                    "value": [
                        {
                            "name": "Savings Account.png",
                            "url": "http://orlando.com/images/Savings Account.png",
                            "mimeType": "image/png",
                            "size": 90759
                        }
                    ]
                },
                {
                    "key": "question_mBxXzY",
                    "label": "Or link to your motivation",
                    "type": "INPUT_LINK",
                    "value": faker.url()
                },
                {
                    "key": "question_wkNydj",
                    "label": "Or write about your motivation",
                    "type": "TEXTAREA",
                    "value": faker.sentence(100)
                },
                {
                    "key": "question_wvPAG8",
                    "label": "Add a fun fact about yourself",
                    "type": "TEXTAREA",
                    "value": faker.sentence(25)
                },
                {
                    "key": "question_mKV6YK",
                    "label": "What do/did you study?",
                    "type": "CHECKBOXES",
                    "value": random.sample([
                        "2882098f-9237-471c-9cca-fbb94336ec47",
                        "f7faa5fd-f421-4038-bc65-cb705bead0e1",
                        "b7823b1e-eb73-4dcc-930a-85adadddd06f",
                        "b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                        "874b62b3-1777-4bff-a51f-82711657ce3d",
                        "29cdb508-55e0-4a7b-ac40-19d7395bab33",
                        "e9d3143b-97c7-4149-b39f-03e4fa118513",
                        "fe10f00d-2e69-4590-b128-12f170178586",
                        "a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                        "9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                    ], random.randint(1, 10)),
                    "options": [
                        {
                            "id": "2882098f-9237-471c-9cca-fbb94336ec47",
                            "text": "Backend development"
                        },
                        {
                            "id": "f7faa5fd-f421-4038-bc65-cb705bead0e1",
                            "text": "Business management"
                        },
                        {
                            "id": "b7823b1e-eb73-4dcc-930a-85adadddd06f",
                            "text": "Communication Sciences"
                        },
                        {
                            "id": "b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                            "text": "Computer Sciences"
                        },
                        {
                            "id": "874b62b3-1777-4bff-a51f-82711657ce3d",
                            "text": "Design"
                        },
                        {
                            "id": "29cdb508-55e0-4a7b-ac40-19d7395bab33",
                            "text": "Frontend development"
                        },
                        {
                            "id": "e9d3143b-97c7-4149-b39f-03e4fa118513",
                            "text": "Marketing"
                        },
                        {
                            "id": "fe10f00d-2e69-4590-b128-12f170178586",
                            "text": "Photography"
                        },
                        {
                            "id": "a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                            "text": "Videography"
                        },
                        {
                            "id": "9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                            "text": "Other"
                        }
                    ]
                },
                {
                    "key": "question_mKV6YK_2882098f-9237-471c-9cca-fbb94336ec47",
                    "label": "What do/did you study? (Backend development)",
                    "type": "CHECKBOXES",
                    "value": True
                },
                {
                    "key": "question_mKV6YK_f7faa5fd-f421-4038-bc65-cb705bead0e1",
                    "label": "What do/did you study? (Business management)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_b7823b1e-eb73-4dcc-930a-85adadddd06f",
                    "label": "What do/did you study? (Communication Sciences)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                    "label": "What do/did you study? (Computer Sciences)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_874b62b3-1777-4bff-a51f-82711657ce3d",
                    "label": "What do/did you study? (Design)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_29cdb508-55e0-4a7b-ac40-19d7395bab33",
                    "label": "What do/did you study? (Frontend development)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_e9d3143b-97c7-4149-b39f-03e4fa118513",
                    "label": "What do/did you study? (Marketing)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_fe10f00d-2e69-4590-b128-12f170178586",
                    "label": "What do/did you study? (Photography)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                    "label": "What do/did you study? (Videography)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_mKV6YK_9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                    "label": "What do/did you study? (Other)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_wLPbZ2",
                    "label": "What do/did you study?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_npDKbE",
                    "label": "What kind of diploma are you currently going for?",
                    "type": "CHECKBOXES",
                    "value": random.sample([
                        "2856db53-84de-4468-a70f-57eb7ba5ec40",
                        "46570410-5581-4ada-9994-2a03f68f67a3",
                        "567f530f-d285-4e40-858f-df2f7a009e30",
                        "bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                        "ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                        "b6abbd71-7924-4655-a7b0-c51c5126ba52",
                        "1c39739b-29ce-4337-915b-bdf23b7a438d",
                    ], random.randint(1, 7)),
                    "options": [
                        {
                            "id": "2856db53-84de-4468-a70f-57eb7ba5ec40",
                            "text": "A professional Bachelor"
                        },
                        {
                            "id": "46570410-5581-4ada-9994-2a03f68f67a3",
                            "text": "An academic Bachelor"
                        },
                        {
                            "id": "567f530f-d285-4e40-858f-df2f7a009e30",
                            "text": "An associate degree"
                        },
                        {
                            "id": "bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                            "text": "A master's degree"
                        },
                        {
                            "id": "ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                            "text": "Doctoral degree"
                        },
                        {
                            "id": "b6abbd71-7924-4655-a7b0-c51c5126ba52",
                            "text": "No diploma, I am self taught"
                        },
                        {
                            "id": "1c39739b-29ce-4337-915b-bdf23b7a438d",
                            "text": "Other"
                        }
                    ]
                },
                {
                    "key": "question_npDKbE_2856db53-84de-4468-a70f-57eb7ba5ec40",
                    "label": "What kind of diploma are you currently going for? (A professional Bachelor)",
                    "type": "CHECKBOXES",
                    "value": True
                },
                {
                    "key": "question_npDKbE_46570410-5581-4ada-9994-2a03f68f67a3",
                    "label": "What kind of diploma are you currently going for? (An academic Bachelor)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_npDKbE_567f530f-d285-4e40-858f-df2f7a009e30",
                    "label": "What kind of diploma are you currently going for? (An associate degree)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_npDKbE_bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                    "label": "What kind of diploma are you currently going for? (A master's degree)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_npDKbE_ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                    "label": "What kind of diploma are you currently going for? (Doctoral degree)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_npDKbE_b6abbd71-7924-4655-a7b0-c51c5126ba52",
                    "label": "What kind of diploma are you currently going for? (No diploma, I am self taught)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_npDKbE_1c39739b-29ce-4337-915b-bdf23b7a438d",
                    "label": "What kind of diploma are you currently going for? (Other)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_319lAL",
                    "label": "What kind of diploma are you currently going for?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_wMEbe0",
                    "label": "How many years does your degree take?",
                    "type": "INPUT_NUMBER",
                    "value": random.randint(2, 7)
                },
                {
                    "key": "question_mJO697",
                    "label": "Which year of your degree are you in?",
                    "type": "INPUT_TEXT",
                    "value": random.randint(2, 7)
                },
                {
                    "key": "question_wg90DK",
                    "label": "What is the name of your college or university?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_3yJ6PW",
                    "label": "Which role are you applying for?",
                    "type": "CHECKBOXES",
                    "value": random.sample([
                        "7ab99307-9377-4b16-bb7a-91172d69c417",
                        "c9a3aa50-7117-448f-9966-3f946731e79e",
                        "7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                        "b8e4905a-fb22-4608-87db-f604ac9ad072",
                        "8421a8c4-01e1-43a6-9973-77af251ddcb2",
                        "8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                        "e5ede7d5-c874-4f93-b995-57bcd6928dad",
                        "c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                        "8c9800db-e9cc-42ce-a87b-f4c42755224f",
                        "8b54310e-70f2-410e-81b5-63ead19a2542",
                        "b96b05a6-5171-4318-8f5c-245b530695dd",
                    ], random.randint(1, 11)),
                    "options": [
                        {
                            "id": "7ab99307-9377-4b16-bb7a-91172d69c417",
                            "text": "Front-end developer"
                        },
                        {
                            "id": "c9a3aa50-7117-448f-9966-3f946731e79e",
                            "text": "Back-end developer"
                        },
                        {
                            "id": "7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                            "text": "UX / UI designer"
                        },
                        {
                            "id": "b8e4905a-fb22-4608-87db-f604ac9ad072",
                            "text": "Graphic designer"
                        },
                        {
                            "id": "8421a8c4-01e1-43a6-9973-77af251ddcb2",
                            "text": "Business Modeller"
                        },
                        {
                            "id": "8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                            "text": "Storyteller"
                        },
                        {
                            "id": "e5ede7d5-c874-4f93-b995-57bcd6928dad",
                            "text": "Marketer"
                        },
                        {
                            "id": "c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                            "text": "Copywriter"
                        },
                        {
                            "id": "8c9800db-e9cc-42ce-a87b-f4c42755224f",
                            "text": "Video editor"
                        },
                        {
                            "id": "8b54310e-70f2-410e-81b5-63ead19a2542",
                            "text": "Photographer"
                        },
                        {
                            "id": "b96b05a6-5171-4318-8f5c-245b530695dd",
                            "text": "Other"
                        }
                    ]
                },
                {
                    "key": "question_3yJ6PW_7ab99307-9377-4b16-bb7a-91172d69c417",
                    "label": "Which role are you applying for? (Front-end developer)",
                    "type": "CHECKBOXES",
                    "value": True
                },
                {
                    "key": "question_3yJ6PW_c9a3aa50-7117-448f-9966-3f946731e79e",
                    "label": "Which role are you applying for? (Back-end developer)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                    "label": "Which role are you applying for? (UX / UI designer)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_b8e4905a-fb22-4608-87db-f604ac9ad072",
                    "label": "Which role are you applying for? (Graphic designer)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_8421a8c4-01e1-43a6-9973-77af251ddcb2",
                    "label": "Which role are you applying for? (Business Modeller)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                    "label": "Which role are you applying for? (Storyteller)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_e5ede7d5-c874-4f93-b995-57bcd6928dad",
                    "label": "Which role are you applying for? (Marketer)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                    "label": "Which role are you applying for? (Copywriter)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_8c9800db-e9cc-42ce-a87b-f4c42755224f",
                    "label": "Which role are you applying for? (Video editor)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_8b54310e-70f2-410e-81b5-63ead19a2542",
                    "label": "Which role are you applying for? (Photographer)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3yJ6PW_b96b05a6-5171-4318-8f5c-245b530695dd",
                    "label": "Which role are you applying for? (Other)",
                    "type": "CHECKBOXES",
                    "value": False
                },
                {
                    "key": "question_3X4DxV",
                    "label": "Which role are you applying for that is not in the list above?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_w8ZKNo",
                    "label": "Which skill would you list as your best one?",
                    "type": "INPUT_TEXT",
                    "value": faker.sentence(5)
                },
                {
                    "key": "question_n0exVQ",
                    "label": "Have you participated in osoc before?",
                    "type": "MULTIPLE_CHOICE",
                    "value": random.choice([
                        "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                        "626e3879-1ffe-4544-a2a1-05a6b5154fc3",
                    ]),
                    "options": [
                        {
                            "id": "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                            "text": "No, it's my first time participating in osoc"
                        },
                        {
                            "id": "626e3879-1ffe-4544-a2a1-05a6b5154fc3",
                            "text": "Yes, I have been part of osoc before"
                        }
                    ]
                },
                {
                    "key": "question_wz7qEE",
                    "label": "Would you like to be a student coach this year?",
                    "type": "MULTIPLE_CHOICE",
                    "value": [
                        "4577f09c-0ec2-4887-b164-79bb536470c4",
                        "ca473ac4-eb45-486d-aacb-c3800b370e71"
                    ][0 if not wants_to_be_student_coach else 1],
                    "options": [
                        {
                            "id": "4577f09c-0ec2-4887-b164-79bb536470c4",
                            "text": "No, I don't want to be a student coach"
                        },
                        {
                            "id": "ca473ac4-eb45-486d-aacb-c3800b370e71",
                            "text": "Yes, I'd like to be a student coach"
                        }
                    ]
                }
            ]
        }
    }


WEBHOOK_EVENT_BAD_FORMAT = {
    "eventId": "5933d05a-b197-45ec-b95c-30c5be43fc80",
    "createdAt": "2022-03-03T10:20:00.859Z",
    "dataa": {  # Changed this.
        "responseId": "85e41402-b5b9-4a24-ac0e-344caa33f985",
        "submissionId": "wkv6d3",
        "respondentId": "63xOJm",
        "formId": "wkjyM3",
        "formName": "#osoc22 student application form",
        "createdAt": "2021-05-12T11:52:57.879Z",
        "fields": [
            {
                "key": "question_nGRzxz",
                "label": "Will you live in Belgium in July 2022?*",
                "type": "MULTIPLE_CHOICE",
                "value": "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                "options": [
                    {
                        "id": "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                        "text": "Yes"
                    },
                    {
                        "id": "444fd1f8-756a-4a24-8189-a306c0fe94b0",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_mO7zDA",
                "label": "Are you able to work 128 hours with a student employment agreement, or as a volunteer?*",
                "type": "MULTIPLE_CHOICE",
                "value": "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                "options": [
                    {
                        "id": "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                        "text": "Yes, I can work with a student employment agreement in Belgium"
                    },
                    {
                        "id": "5b519077-25c5-4d20-ab7f-2da844989ddb",
                        "text": "Yes, I can work as a volunteer in Belgium"
                    },
                    {
                        "id": "f7fc01d2-a274-413b-8ea2-c0630d075e03",
                        "text": "No – but I would like to join this experience for free"
                    },
                    {
                        "id": "398e4fe0-c307-4bce-9120-2079d35fe184",
                        "text": "No, I won’t be able to work as a student, as a volunteer or for free."
                    }
                ]
            },
            {
                "key": "question_mVz0Ll",
                "label": "Can you work during the month of July, Monday through Thursday (~09:00 to 17:00)?*",
                "type": "MULTIPLE_CHOICE",
                "value": "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                "options": [
                    {
                        "id": "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                        "text": "Yes"
                    },
                    {
                        "id": "748287a7-7b52-4746-8c5f-323caedcbbee",
                        "text": "No, I wouldn't be able to work for the majority of days."
                    }
                ]
            },
            {
                "key": "question_nPz6d0",
                "label": "Are there any responsibilities you might have which could hinder you during the day?",
                "type": "TEXTAREA",
                "value": "Fresh"
            },
            {
                "key": "question_3ExXkL",
                "label": "Birth name",
                "type": "INPUT_TEXT",
                "value": "Checking Account"
            },
            {
                "key": "question_nro6jL",
                "label": "Last name",
                "type": "INPUT_TEXT",
                "value": "Generic Concrete Bike"
            },
            {
                "key": "question_w4K84o",
                "label": "Would you like to be called by a different name than your birth name?",
                "type": "MULTIPLE_CHOICE",
                "value": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                "options": [
                    {
                        "id": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                        "text": "Yes"
                    },
                    {
                        "id": "10532c12-72fe-46c1-aca6-54e6185d385d",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_3jlya9",
                "label": "How would you like to be called?",
                "type": "INPUT_TEXT",
                "value": "calculate"
            },
            {
                "key": "question_w2KeEb",
                "label": "What is your gender?",
                "type": "MULTIPLE_CHOICE",
                "value": "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                "options": [
                    {
                        "id": "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                        "text": "Female"
                    },
                    {
                        "id": "3b3e4851-354d-4135-92e0-7cab57041fc5",
                        "text": "Male"
                    },
                    {
                        "id": "ae4a4c95-4f22-48b9-892e-80d38bbe7ef1",
                        "text": "Transgender"
                    },
                    {
                        "id": "20ba24a6-b52a-43ae-a517-556b139a8984",
                        "text": "Rather not say"
                    }
                ]
            },
            {
                "key": "question_3xJpX9",
                "label": "Would you like to add your pronouns?",
                "type": "MULTIPLE_CHOICE",
                "value": "980614af-52d8-45d9-acb6-9d76952a86f1",
                "options": [
                    {
                        "id": "980614af-52d8-45d9-acb6-9d76952a86f1",
                        "text": "Yes"
                    },
                    {
                        "id": "ea012b47-896a-4264-b876-35c7e7392a06",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_mZ2Njv",
                "label": "Which pronouns do you prefer?",
                "type": "MULTIPLE_CHOICE",
                "value": "7719f945-47ca-4166-9aa3-a3a2e1387009",
                "options": [
                    {
                        "id": "7719f945-47ca-4166-9aa3-a3a2e1387009",
                        "text": "she/her/hers"
                    },
                    {
                        "id": "d9245c04-4abe-488e-a884-17f6c501c1eb",
                        "text": "he/him/his"
                    },
                    {
                        "id": "b78cb089-3e57-484e-bb86-03f3cc753571",
                        "text": "they/them/theirs"
                    },
                    {
                        "id": "2d74b670-9f74-481a-bd2f-b8b06668f0a4",
                        "text": "ze/hir/hir "
                    },
                    {
                        "id": "a9145194-f930-436e-b0e0-340e7c3fac3e",
                        "text": "by firstname"
                    },
                    {
                        "id": "e6d5eae6-9340-44ca-a268-934e53ebf707",
                        "text": "by call name"
                    },
                    {
                        "id": "ac94baff-9650-4751-83fe-b8315ddedb80",
                        "text": "other"
                    }
                ]
            },
            {
                "key": "question_3N76pb",
                "label": "Enter your pronouns",
                "type": "INPUT_TEXT",
                "value": "Administrator"
            },
            {
                "key": "question_3qRd4k",
                "label": "What language are you most fluent in?",
                "type": "MULTIPLE_CHOICE",
                "value": "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                "options": [
                    {
                        "id": "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                        "text": "Dutch"
                    },
                    {
                        "id": "aafb7b8e-e437-440c-a3c6-22a2b61da769",
                        "text": "English"
                    },
                    {
                        "id": "06efe9b0-8187-4f8c-9f88-53da49177a28",
                        "text": "French"
                    },
                    {
                        "id": "f4b3f9c9-525e-4bd2-949c-3b52e04477ca",
                        "text": "German"
                    },
                    {
                        "id": "b6902bde-6134-442d-a8a8-18e882e3e09d",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_wQ7DKk",
                "label": "What language are you most fluent in?",
                "type": "INPUT_TEXT",
                "value": "killer"
            },
            {
                "key": "question_n97Wq4",
                "label": "How would you rate your English?",
                "type": "MULTIPLE_CHOICE",
                "value": "0288cfa1-a19a-40f4-a172-8b9335152d57",
                "options": [
                    {
                        "id": "0288cfa1-a19a-40f4-a172-8b9335152d57",
                        "text": "★ I can understand your form, but it is hard for me to reply."
                    },
                    {
                        "id": "9de70dc1-c4b6-4734-84d1-3e3a2a29a70f",
                        "text": "★★ I can have simple conversations."
                    },
                    {
                        "id": "a5464911-6714-490b-a370-eb3de514573a",
                        "text": "★★★ I can express myself, understand people and get a point across."
                    },
                    {
                        "id": "10ccead0-4539-4695-978b-16a24c1a1fe1",
                        "text": "★★★★ I can have extensive and complicated conversations."
                    },
                    {
                        "id": "784e392f-9e56-4bba-8cdd-1a85e3194352",
                        "text": "★★★★★ I am fluent."
                    }
                ]
            },
            {
                "key": "question_mea6qo",
                "label": "Phone number",
                "type": "INPUT_PHONE_NUMBER",
                "value": "1-445-703-7597"
            },
            {
                "key": "question_nW8NOQ",
                "label": "Your email address\n",
                "type": "INPUT_EMAIL",
                "value": "Lola66@gmail.com"
            },
            {
                "key": "question_wa26Qy",
                "label": "Upload your CV – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "panel.png",
                        "url": "https://rubye.net/images/panel.png",
                        "mimeType": "image/png",
                        "size": 4033
                    }
                ]
            },
            {
                "key": "question_m6Z785",
                "label": "Or link to your CV",
                "type": "INPUT_LINK",
                "value": "http://kristoffer.net"
            },
            {
                "key": "question_w7NWRz",
                "label": "Upload your portfolio – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "Tuna.png",
                        "url": "http://eliza.name/images/Tuna.png",
                        "mimeType": "image/png",
                        "size": 43843
                    }
                ]
            },
            {
                "key": "question_wbW75E",
                "label": "Or link to your portfolio / GitHub",
                "type": "INPUT_LINK",
                "value": "http://miguel.com"
            },
            {
                "key": "question_wABd7N",
                "label": "Upload your motivation – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "Savings Account.png",
                        "url": "http://orlando.com/images/Savings Account.png",
                        "mimeType": "image/png",
                        "size": 90759
                    }
                ]
            },
            {
                "key": "question_mBxXzY",
                "label": "Or link to your motivation",
                "type": "INPUT_LINK",
                "value": "https://douglas.org"
            },
            {
                "key": "question_wkNydj",
                "label": "Or write about your motivation",
                "type": "TEXTAREA",
                "value": "Developer"
            },
            {
                "key": "question_wvPAG8",
                "label": "Add a fun fact about yourself",
                "type": "TEXTAREA",
                "value": "Intelligent"
            },
            {
                "key": "question_mKV6YK",
                "label": "What do/did you study?",
                "type": "CHECKBOXES",
                "value": [
                    "2882098f-9237-471c-9cca-fbb94336ec47"
                ],
                "options": [
                    {
                        "id": "2882098f-9237-471c-9cca-fbb94336ec47",
                        "text": "Backend development"
                    },
                    {
                        "id": "f7faa5fd-f421-4038-bc65-cb705bead0e1",
                        "text": "Business management"
                    },
                    {
                        "id": "b7823b1e-eb73-4dcc-930a-85adadddd06f",
                        "text": "Communication Sciences"
                    },
                    {
                        "id": "b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                        "text": "Computer Sciences"
                    },
                    {
                        "id": "874b62b3-1777-4bff-a51f-82711657ce3d",
                        "text": "Design"
                    },
                    {
                        "id": "29cdb508-55e0-4a7b-ac40-19d7395bab33",
                        "text": "Frontend development"
                    },
                    {
                        "id": "e9d3143b-97c7-4149-b39f-03e4fa118513",
                        "text": "Marketing"
                    },
                    {
                        "id": "fe10f00d-2e69-4590-b128-12f170178586",
                        "text": "Photography"
                    },
                    {
                        "id": "a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                        "text": "Videography"
                    },
                    {
                        "id": "9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_mKV6YK_2882098f-9237-471c-9cca-fbb94336ec47",
                "label": "What do/did you study? (Backend development)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_mKV6YK_f7faa5fd-f421-4038-bc65-cb705bead0e1",
                "label": "What do/did you study? (Business management)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_b7823b1e-eb73-4dcc-930a-85adadddd06f",
                "label": "What do/did you study? (Communication Sciences)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                "label": "What do/did you study? (Computer Sciences)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_874b62b3-1777-4bff-a51f-82711657ce3d",
                "label": "What do/did you study? (Design)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_29cdb508-55e0-4a7b-ac40-19d7395bab33",
                "label": "What do/did you study? (Frontend development)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_e9d3143b-97c7-4149-b39f-03e4fa118513",
                "label": "What do/did you study? (Marketing)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_fe10f00d-2e69-4590-b128-12f170178586",
                "label": "What do/did you study? (Photography)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                "label": "What do/did you study? (Videography)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                "label": "What do/did you study? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_wLPbZ2",
                "label": "What do/did you study?",
                "type": "INPUT_TEXT",
                "value": "Plastic"
            },
            {
                "key": "question_npDKbE",
                "label": "What kind of diploma are you currently going for?",
                "type": "CHECKBOXES",
                "value": [
                    "2856db53-84de-4468-a70f-57eb7ba5ec40"
                ],
                "options": [
                    {
                        "id": "2856db53-84de-4468-a70f-57eb7ba5ec40",
                        "text": "A professional Bachelor"
                    },
                    {
                        "id": "46570410-5581-4ada-9994-2a03f68f67a3",
                        "text": "An academic Bachelor"
                    },
                    {
                        "id": "567f530f-d285-4e40-858f-df2f7a009e30",
                        "text": "An associate degree"
                    },
                    {
                        "id": "bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                        "text": "A master's degree"
                    },
                    {
                        "id": "ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                        "text": "Doctoral degree"
                    },
                    {
                        "id": "b6abbd71-7924-4655-a7b0-c51c5126ba52",
                        "text": "No diploma, I am self taught"
                    },
                    {
                        "id": "1c39739b-29ce-4337-915b-bdf23b7a438d",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_npDKbE_2856db53-84de-4468-a70f-57eb7ba5ec40",
                "label": "What kind of diploma are you currently going for? (A professional Bachelor)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_npDKbE_46570410-5581-4ada-9994-2a03f68f67a3",
                "label": "What kind of diploma are you currently going for? (An academic Bachelor)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_567f530f-d285-4e40-858f-df2f7a009e30",
                "label": "What kind of diploma are you currently going for? (An associate degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                "label": "What kind of diploma are you currently going for? (A master's degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                "label": "What kind of diploma are you currently going for? (Doctoral degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_b6abbd71-7924-4655-a7b0-c51c5126ba52",
                "label": "What kind of diploma are you currently going for? (No diploma, I am self taught)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_1c39739b-29ce-4337-915b-bdf23b7a438d",
                "label": "What kind of diploma are you currently going for? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_319lAL",
                "label": "What kind of diploma are you currently going for?",
                "type": "INPUT_TEXT",
                "value": "clear-thinking"
            },
            {
                "key": "question_wMEbe0",
                "label": "How many years does your degree take?",
                "type": "INPUT_NUMBER",
                "value": 1
            },
            {
                "key": "question_mJO697",
                "label": "Which year of your degree are you in?",
                "type": "INPUT_TEXT",
                "value": "architectures"
            },
            {
                "key": "question_wg90DK",
                "label": "What is the name of your college or university?",
                "type": "INPUT_TEXT",
                "value": "synergies"
            },
            {
                "key": "question_3yJ6PW",
                "label": "Which role are you applying for?",
                "type": "CHECKBOXES",
                "value": [
                    "7ab99307-9377-4b16-bb7a-91172d69c417"
                ],
                "options": [
                    {
                        "id": "7ab99307-9377-4b16-bb7a-91172d69c417",
                        "text": "Front-end developer"
                    },
                    {
                        "id": "c9a3aa50-7117-448f-9966-3f946731e79e",
                        "text": "Back-end developer"
                    },
                    {
                        "id": "7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                        "text": "UX / UI designer"
                    },
                    {
                        "id": "b8e4905a-fb22-4608-87db-f604ac9ad072",
                        "text": "Graphic designer"
                    },
                    {
                        "id": "8421a8c4-01e1-43a6-9973-77af251ddcb2",
                        "text": "Business Modeller"
                    },
                    {
                        "id": "8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                        "text": "Storyteller"
                    },
                    {
                        "id": "e5ede7d5-c874-4f93-b995-57bcd6928dad",
                        "text": "Marketer"
                    },
                    {
                        "id": "c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                        "text": "Copywriter"
                    },
                    {
                        "id": "8c9800db-e9cc-42ce-a87b-f4c42755224f",
                        "text": "Video editor"
                    },
                    {
                        "id": "8b54310e-70f2-410e-81b5-63ead19a2542",
                        "text": "Photographer"
                    },
                    {
                        "id": "b96b05a6-5171-4318-8f5c-245b530695dd",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_3yJ6PW_7ab99307-9377-4b16-bb7a-91172d69c417",
                "label": "Which role are you applying for? (Front-end developer)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_3yJ6PW_c9a3aa50-7117-448f-9966-3f946731e79e",
                "label": "Which role are you applying for? (Back-end developer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                "label": "Which role are you applying for? (UX / UI designer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_b8e4905a-fb22-4608-87db-f604ac9ad072",
                "label": "Which role are you applying for? (Graphic designer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8421a8c4-01e1-43a6-9973-77af251ddcb2",
                "label": "Which role are you applying for? (Business Modeller)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                "label": "Which role are you applying for? (Storyteller)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_e5ede7d5-c874-4f93-b995-57bcd6928dad",
                "label": "Which role are you applying for? (Marketer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                "label": "Which role are you applying for? (Copywriter)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8c9800db-e9cc-42ce-a87b-f4c42755224f",
                "label": "Which role are you applying for? (Video editor)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8b54310e-70f2-410e-81b5-63ead19a2542",
                "label": "Which role are you applying for? (Photographer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_b96b05a6-5171-4318-8f5c-245b530695dd",
                "label": "Which role are you applying for? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3X4DxV",
                "label": "Which role are you applying for that is not in the list above?",
                "type": "INPUT_TEXT",
                "value": "indigo"
            },
            {
                "key": "question_w8ZKNo",
                "label": "Which skill would you list as your best one?",
                "type": "INPUT_TEXT",
                "value": "invoice"
            },
            {
                "key": "question_n0exVQ",
                "label": "Have you participated in osoc before?",
                "type": "MULTIPLE_CHOICE",
                "value": "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                "options": [
                    {
                        "id": "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                        "text": "No, it's my first time participating in osoc"
                    },
                    {
                        "id": "626e3879-1ffe-4544-a2a1-05a6b5154fc3",
                        "text": "Yes, I have been part of osoc before"
                    }
                ]
            },
            {
                "key": "question_wz7qEE",
                "label": "Would you like to be a student coach this year?",
                "type": "MULTIPLE_CHOICE",
                "value": "4577f09c-0ec2-4887-b164-79bb536470c4",
                "options": [
                    {
                        "id": "4577f09c-0ec2-4887-b164-79bb536470c4",
                        "text": "No, I don't want to be a student coach"
                    },
                    {
                        "id": "ca473ac4-eb45-486d-aacb-c3800b370e71",
                        "text": "Yes, I'd like to be a student coach"
                    }
                ]
            }
        ]
    }
}

WEBHOOK_MISSING_QUESTION = {
    "eventId": "5933d05a-b197-45ec-b95c-30c5be43fc80",
    "createdAt": "2022-03-03T10:20:00.859Z",
    "data": {
        "responseId": "85e41402-b5b9-4a24-ac0e-344caa33f985",
        "submissionId": "wkv6d3",
        "respondentId": "63xOJm",
        "formId": "wkjyM3",
        "formName": "#osoc22 student application form",
        "createdAt": "2021-05-12T11:52:57.879Z",
        "fields": [
            {
                "key": "question_nGRzxz",
                "label": "Will you live in Belgium in July 2022?*",
                "type": "MULTIPLE_CHOICE",
                "value": "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                "options": [
                    {
                        "id": "779e2fe0-64fe-4d87-b337-957c4a0517e3",
                        "text": "Yes"
                    },
                    {
                        "id": "444fd1f8-756a-4a24-8189-a306c0fe94b0",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_mO7zDA",
                "label": "Are you able to work 128 hours with a student employment agreement, or as a volunteer?*",
                "type": "MULTIPLE_CHOICE",
                "value": "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                "options": [
                    {
                        "id": "0bcaf720-2040-4d31-a3e8-59c5644dab9a",
                        "text": "Yes, I can work with a student employment agreement in Belgium"
                    },
                    {
                        "id": "5b519077-25c5-4d20-ab7f-2da844989ddb",
                        "text": "Yes, I can work as a volunteer in Belgium"
                    },
                    {
                        "id": "f7fc01d2-a274-413b-8ea2-c0630d075e03",
                        "text": "No – but I would like to join this experience for free"
                    },
                    {
                        "id": "398e4fe0-c307-4bce-9120-2079d35fe184",
                        "text": "No, I won’t be able to work as a student, as a volunteer or for free."
                    }
                ]
            },
            {
                "key": "question_mVz0Ll",
                "label": "Can you work during the month of July, Monday through Thursday (~09:00 to 17:00)?*",
                "type": "MULTIPLE_CHOICE",
                "value": "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                "options": [
                    {
                        "id": "6d7b21a6-5a78-4d56-89ee-e20fb01b4c25",
                        "text": "Yes"
                    },
                    {
                        "id": "748287a7-7b52-4746-8c5f-323caedcbbee",
                        "text": "No, I wouldn't be able to work for the majority of days."
                    }
                ]
            },
            {
                "key": "question_nPz6d0",
                "label": "Are there any responsibilities you might have which could hinder you during the day?",
                "type": "TEXTAREA",
                "value": "Fresh"
            },
            {
                "key": "question_3ExXkL",
                "label": "Birth name",
                "type": "INPUT_TEXT",
                "value": "Checking Account"
            },
            {
                "key": "question_nro6jL",
                "label": "Last name",
                "type": "INPUT_TEXT",
                "value": "Generic Concrete Bike"
            },
            {
                "key": "question_w4K84o",
                "label": "Would you like to be called by a different name than your birth name?",
                "type": "MULTIPLE_CHOICE",
                "value": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                "options": [
                    {
                        "id": "4e8760d6-4960-404c-82fb-8b2e8dc6af61",
                        "text": "Yes"
                    },
                    {
                        "id": "10532c12-72fe-46c1-aca6-54e6185d385d",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_3jlya9",
                "label": "How would you like to be called?",
                "type": "INPUT_TEXT",
                "value": "calculate"
            },
            {
                "key": "question_w2KeEb",
                "label": "What is your gender?",
                "type": "MULTIPLE_CHOICE",
                "value": "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                "options": [
                    {
                        "id": "dcb028c2-bdd3-4bc6-abe1-3937862a7c8f",
                        "text": "Female"
                    },
                    {
                        "id": "3b3e4851-354d-4135-92e0-7cab57041fc5",
                        "text": "Male"
                    },
                    {
                        "id": "ae4a4c95-4f22-48b9-892e-80d38bbe7ef1",
                        "text": "Transgender"
                    },
                    {
                        "id": "20ba24a6-b52a-43ae-a517-556b139a8984",
                        "text": "Rather not say"
                    }
                ]
            },
            {
                "key": "question_3xJpX9",
                "label": "Would you like to add your pronouns?",
                "type": "MULTIPLE_CHOICE",
                "value": "980614af-52d8-45d9-acb6-9d76952a86f1",
                "options": [
                    {
                        "id": "980614af-52d8-45d9-acb6-9d76952a86f1",
                        "text": "Yes"
                    },
                    {
                        "id": "ea012b47-896a-4264-b876-35c7e7392a06",
                        "text": "No"
                    }
                ]
            },
            {
                "key": "question_mZ2Njv",
                "label": "Which pronouns do you prefer?",
                "type": "MULTIPLE_CHOICE",
                "value": "7719f945-47ca-4166-9aa3-a3a2e1387009",
                "options": [
                    {
                        "id": "7719f945-47ca-4166-9aa3-a3a2e1387009",
                        "text": "she/her/hers"
                    },
                    {
                        "id": "d9245c04-4abe-488e-a884-17f6c501c1eb",
                        "text": "he/him/his"
                    },
                    {
                        "id": "b78cb089-3e57-484e-bb86-03f3cc753571",
                        "text": "they/them/theirs"
                    },
                    {
                        "id": "2d74b670-9f74-481a-bd2f-b8b06668f0a4",
                        "text": "ze/hir/hir "
                    },
                    {
                        "id": "a9145194-f930-436e-b0e0-340e7c3fac3e",
                        "text": "by firstname"
                    },
                    {
                        "id": "e6d5eae6-9340-44ca-a268-934e53ebf707",
                        "text": "by call name"
                    },
                    {
                        "id": "ac94baff-9650-4751-83fe-b8315ddedb80",
                        "text": "other"
                    }
                ]
            },
            {
                "key": "question_3N76pb",
                "label": "Enter your pronouns",
                "type": "INPUT_TEXT",
                "value": "Administrator"
            },
            {
                "key": "question_3qRd4k",
                "label": "What language are you most fluent in?",
                "type": "MULTIPLE_CHOICE",
                "value": "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                "options": [
                    {
                        "id": "7f4d9b81-fb56-4a07-b878-9b2ac913348b",
                        "text": "Dutch"
                    },
                    {
                        "id": "aafb7b8e-e437-440c-a3c6-22a2b61da769",
                        "text": "English"
                    },
                    {
                        "id": "06efe9b0-8187-4f8c-9f88-53da49177a28",
                        "text": "French"
                    },
                    {
                        "id": "f4b3f9c9-525e-4bd2-949c-3b52e04477ca",
                        "text": "German"
                    },
                    {
                        "id": "b6902bde-6134-442d-a8a8-18e882e3e09d",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_wQ7DKk",
                "label": "What language are you most fluent in?",
                "type": "INPUT_TEXT",
                "value": "killer"
            },
            {
                "key": "question_n97Wq4",
                "label": "How would you rate your English?",
                "type": "MULTIPLE_CHOICE",
                "value": "0288cfa1-a19a-40f4-a172-8b9335152d57",
                "options": [
                    {
                        "id": "0288cfa1-a19a-40f4-a172-8b9335152d57",
                        "text": "★ I can understand your form, but it is hard for me to reply."
                    },
                    {
                        "id": "9de70dc1-c4b6-4734-84d1-3e3a2a29a70f",
                        "text": "★★ I can have simple conversations."
                    },
                    {
                        "id": "a5464911-6714-490b-a370-eb3de514573a",
                        "text": "★★★ I can express myself, understand people and get a point across."
                    },
                    {
                        "id": "10ccead0-4539-4695-978b-16a24c1a1fe1",
                        "text": "★★★★ I can have extensive and complicated conversations."
                    },
                    {
                        "id": "784e392f-9e56-4bba-8cdd-1a85e3194352",
                        "text": "★★★★★ I am fluent."
                    }
                ]
            },
            {
                "key": "question_mea6qo",
                "label": "Phone number",
                "type": "INPUT_PHONE_NUMBER",
                "value": "1-445-703-7597"
            },
            {
                "key": "question_nW8NOQ",
                "label": "Your email address\n",
                "type": "INPUT_EMAIL",
                "value": "Lola66@gmail.com"
            },
            {
                "key": "question_wa26Qy",
                "label": "Upload your CV – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "panel.png",
                        "url": "https://rubye.net/images/panel.png",
                        "mimeType": "image/png",
                        "size": 4033
                    }
                ]
            },
            {
                "key": "question_m6Z785",
                "label": "Or link to your CV",
                "type": "INPUT_LINK",
                "value": "http://kristoffer.net"
            },
            {
                "key": "question_w7NWRz",
                "label": "Upload your portfolio – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "Tuna.png",
                        "url": "http://eliza.name/images/Tuna.png",
                        "mimeType": "image/png",
                        "size": 43843
                    }
                ]
            },
            {
                "key": "question_wbW75E",
                "label": "Or link to your portfolio / GitHub",
                "type": "INPUT_LINK",
                "value": "http://miguel.com"
            },
            {
                "key": "question_wABd7N",
                "label": "Upload your motivation – size limit 10MB",
                "type": "FILE_UPLOAD",
                "value": [
                    {
                        "name": "Savings Account.png",
                        "url": "http://orlando.com/images/Savings Account.png",
                        "mimeType": "image/png",
                        "size": 90759
                    }
                ]
            },
            {
                "key": "question_mBxXzY",
                "label": "Or link to your motivation",
                "type": "INPUT_LINK",
                "value": "https://douglas.org"
            },
            {
                "key": "question_wkNydj",
                "label": "Or write about your motivation",
                "type": "TEXTAREA",
                "value": "Developer"
            },
            {
                "key": "question_wvPAG8",
                "label": "Add a fun fact about yourself",
                "type": "TEXTAREA",
                "value": "Intelligent"
            },
            {
                "key": "question_mKV6YK",
                "label": "What do/did you study?",
                "type": "CHECKBOXES",
                "value": [
                    "2882098f-9237-471c-9cca-fbb94336ec47"
                ],
                "options": [
                    {
                        "id": "2882098f-9237-471c-9cca-fbb94336ec47",
                        "text": "Backend development"
                    },
                    {
                        "id": "f7faa5fd-f421-4038-bc65-cb705bead0e1",
                        "text": "Business management"
                    },
                    {
                        "id": "b7823b1e-eb73-4dcc-930a-85adadddd06f",
                        "text": "Communication Sciences"
                    },
                    {
                        "id": "b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                        "text": "Computer Sciences"
                    },
                    {
                        "id": "874b62b3-1777-4bff-a51f-82711657ce3d",
                        "text": "Design"
                    },
                    {
                        "id": "29cdb508-55e0-4a7b-ac40-19d7395bab33",
                        "text": "Frontend development"
                    },
                    {
                        "id": "e9d3143b-97c7-4149-b39f-03e4fa118513",
                        "text": "Marketing"
                    },
                    {
                        "id": "fe10f00d-2e69-4590-b128-12f170178586",
                        "text": "Photography"
                    },
                    {
                        "id": "a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                        "text": "Videography"
                    },
                    {
                        "id": "9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_mKV6YK_2882098f-9237-471c-9cca-fbb94336ec47",
                "label": "What do/did you study? (Backend development)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_mKV6YK_f7faa5fd-f421-4038-bc65-cb705bead0e1",
                "label": "What do/did you study? (Business management)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_b7823b1e-eb73-4dcc-930a-85adadddd06f",
                "label": "What do/did you study? (Communication Sciences)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_b562c0a2-40af-4f51-8d37-50e1dc3f96eb",
                "label": "What do/did you study? (Computer Sciences)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_874b62b3-1777-4bff-a51f-82711657ce3d",
                "label": "What do/did you study? (Design)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_29cdb508-55e0-4a7b-ac40-19d7395bab33",
                "label": "What do/did you study? (Frontend development)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_e9d3143b-97c7-4149-b39f-03e4fa118513",
                "label": "What do/did you study? (Marketing)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_fe10f00d-2e69-4590-b128-12f170178586",
                "label": "What do/did you study? (Photography)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_a9e33c5a-a8e6-4c79-b262-37fa9107ac04",
                "label": "What do/did you study? (Videography)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_mKV6YK_9061ff92-8dfa-4e40-8492-c2905fe2ca49",
                "label": "What do/did you study? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_wLPbZ2",
                "label": "What do/did you study?",
                "type": "INPUT_TEXT",
                "value": "Plastic"
            },
            {
                "key": "question_npDKbE",
                "label": "What kind of diploma are you currently going for?",
                "type": "CHECKBOXES",
                "value": [
                    "2856db53-84de-4468-a70f-57eb7ba5ec40"
                ],
                "options": [
                    {
                        "id": "2856db53-84de-4468-a70f-57eb7ba5ec40",
                        "text": "A professional Bachelor"
                    },
                    {
                        "id": "46570410-5581-4ada-9994-2a03f68f67a3",
                        "text": "An academic Bachelor"
                    },
                    {
                        "id": "567f530f-d285-4e40-858f-df2f7a009e30",
                        "text": "An associate degree"
                    },
                    {
                        "id": "bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                        "text": "A master's degree"
                    },
                    {
                        "id": "ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                        "text": "Doctoral degree"
                    },
                    {
                        "id": "b6abbd71-7924-4655-a7b0-c51c5126ba52",
                        "text": "No diploma, I am self taught"
                    },
                    {
                        "id": "1c39739b-29ce-4337-915b-bdf23b7a438d",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_npDKbE_2856db53-84de-4468-a70f-57eb7ba5ec40",
                "label": "What kind of diploma are you currently going for? (A professional Bachelor)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_npDKbE_46570410-5581-4ada-9994-2a03f68f67a3",
                "label": "What kind of diploma are you currently going for? (An academic Bachelor)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_567f530f-d285-4e40-858f-df2f7a009e30",
                "label": "What kind of diploma are you currently going for? (An associate degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_bd722bf4-ed2f-4dd3-8aa4-b9f741c3d0ca",
                "label": "What kind of diploma are you currently going for? (A master's degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_ea137e4d-c7c9-4f9e-b6a5-96e2239e5560",
                "label": "What kind of diploma are you currently going for? (Doctoral degree)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_b6abbd71-7924-4655-a7b0-c51c5126ba52",
                "label": "What kind of diploma are you currently going for? (No diploma, I am self taught)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_npDKbE_1c39739b-29ce-4337-915b-bdf23b7a438d",
                "label": "What kind of diploma are you currently going for? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_319lAL",
                "label": "What kind of diploma are you currently going for?",
                "type": "INPUT_TEXT",
                "value": "clear-thinking"
            },
            {
                "key": "question_wMEbe0",
                "label": "How many years does your degree take?",
                "type": "INPUT_NUMBER",
                "value": 1
            },
            {
                "key": "question_mJO697",
                "label": "Which year of your degree are you in?",
                "type": "INPUT_TEXT",
                "value": "architectures"
            },
            {
                "key": "question_wg90DK",
                "label": "What is the name of your college or university?",
                "type": "INPUT_TEXT",
                "value": "synergies"
            },
            {
                "key": "question_3yJ6PW",
                "label": "Which role are you applying for?",
                "type": "CHECKBOXES",
                "value": [
                    "7ab99307-9377-4b16-bb7a-91172d69c417"
                ],
                "options": [
                    {
                        "id": "7ab99307-9377-4b16-bb7a-91172d69c417",
                        "text": "Front-end developer"
                    },
                    {
                        "id": "c9a3aa50-7117-448f-9966-3f946731e79e",
                        "text": "Back-end developer"
                    },
                    {
                        "id": "7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                        "text": "UX / UI designer"
                    },
                    {
                        "id": "b8e4905a-fb22-4608-87db-f604ac9ad072",
                        "text": "Graphic designer"
                    },
                    {
                        "id": "8421a8c4-01e1-43a6-9973-77af251ddcb2",
                        "text": "Business Modeller"
                    },
                    {
                        "id": "8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                        "text": "Storyteller"
                    },
                    {
                        "id": "e5ede7d5-c874-4f93-b995-57bcd6928dad",
                        "text": "Marketer"
                    },
                    {
                        "id": "c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                        "text": "Copywriter"
                    },
                    {
                        "id": "8c9800db-e9cc-42ce-a87b-f4c42755224f",
                        "text": "Video editor"
                    },
                    {
                        "id": "8b54310e-70f2-410e-81b5-63ead19a2542",
                        "text": "Photographer"
                    },
                    {
                        "id": "b96b05a6-5171-4318-8f5c-245b530695dd",
                        "text": "Other"
                    }
                ]
            },
            {
                "key": "question_3yJ6PW_7ab99307-9377-4b16-bb7a-91172d69c417",
                "label": "Which role are you applying for? (Front-end developer)",
                "type": "CHECKBOXES",
                "value": True
            },
            {
                "key": "question_3yJ6PW_c9a3aa50-7117-448f-9966-3f946731e79e",
                "label": "Which role are you applying for? (Back-end developer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_7f53e36f-4c84-4e00-baf9-0881e0e6ab51",
                "label": "Which role are you applying for? (UX / UI designer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_b8e4905a-fb22-4608-87db-f604ac9ad072",
                "label": "Which role are you applying for? (Graphic designer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8421a8c4-01e1-43a6-9973-77af251ddcb2",
                "label": "Which role are you applying for? (Business Modeller)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8c1f1b4e-5004-43c8-8aa5-0241ed14d759",
                "label": "Which role are you applying for? (Storyteller)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_e5ede7d5-c874-4f93-b995-57bcd6928dad",
                "label": "Which role are you applying for? (Marketer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_c4ee7339-dff5-48c6-9d66-2a1d682dbfea",
                "label": "Which role are you applying for? (Copywriter)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8c9800db-e9cc-42ce-a87b-f4c42755224f",
                "label": "Which role are you applying for? (Video editor)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_8b54310e-70f2-410e-81b5-63ead19a2542",
                "label": "Which role are you applying for? (Photographer)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3yJ6PW_b96b05a6-5171-4318-8f5c-245b530695dd",
                "label": "Which role are you applying for? (Other)",
                "type": "CHECKBOXES",
                "value": False
            },
            {
                "key": "question_3X4DxV",
                "label": "Which role are you applying for that is not in the list above?",
                "type": "INPUT_TEXT",
                "value": "indigo"
            },
            {
                "key": "question_w8ZKNo",
                "label": "Which skill would you list as your best one?",
                "type": "INPUT_TEXT",
                "value": "invoice"
            },
            {
                "key": "question_n0exVQ",
                "label": "Have you participated in osoc before?",
                "type": "MULTIPLE_CHOICE",
                "value": "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                "options": [
                    {
                        "id": "89597a5d-bf59-41d0-88b1-cbce36cee12d",
                        "text": "No, it's my first time participating in osoc"
                    },
                    {
                        "id": "626e3879-1ffe-4544-a2a1-05a6b5154fc3",
                        "text": "Yes, I have been part of osoc before"
                    }
                ]
            },
            # {
            #     "key": "question_wz7qEE",
            #     "label": "Would you like to be a student coach this year?",
            #     "type": "MULTIPLE_CHOICE",
            #     "value": "4577f09c-0ec2-4887-b164-79bb536470c4",
            #     "options": [
            #         {
            #             "id": "4577f09c-0ec2-4887-b164-79bb536470c4",
            #             "text": "No, I don't want to be a student coach"
            #         },
            #         {
            #             "id": "ca473ac4-eb45-486d-aacb-c3800b370e71",
            #             "text": "Yes, I'd like to be a student coach"
            #         }
            #     ]
            # }
        ]
    }
}
