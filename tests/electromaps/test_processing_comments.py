from src.electromaps.run import processing_comments


def test_processing_comments_one_comment() -> None:
    res = processing_comments(
        [{349444:
            [
                {
                    "idcomment": 353292,
                    "comment": "Esto es un p... cachondeo.",
                    "connector": 'null',
                    "score": 'null',
                    "charged": 'null',
                    "created_at": "2023-02-28T15:42:11+0000",
                    "created_by": {
                        "id": 173202,
                        "username": "ToniGonzalez",
                        "avatar": "https://cfassets.electromaps.com/img/account_150x150.png",
                        "electromaps_uuid": "945f2144-92b6-46f6-acf5-78c58a7ad1c5"
                    },
                    "report_status": 'null'
                }
            ]
        }]
    )

    assert res == [{
        'place_id': 349444,
        'comment_id': 353292,
        'author': 'ToniGonzalez',
        'text': 'Esto es un p... cachondeo.',
        'publication_date': '2023-02-28T15:42:11+0000',
        'source': 'electromaps'
    }]


def test_processing_comments_few_comments() -> None:
    res = processing_comments(
        [{349444:
            [
                {
                    "idcomment": 353292,
                    "comment": "Esto es un p... cachondeo.",
                    "connector": 'null',
                    "score": 'null',
                    "charged": 'null',
                    "created_at": "2023-02-28T15:42:11+0000",
                    "created_by": {
                        "id": 173202,
                        "username": "ToniGonzalez",
                        "avatar": "https://cfassets.electromaps.com/img/account_150x150.png",
                        "electromaps_uuid": "945f2144-92b6-46f6-acf5-78c58a7ad1c5"
                    },
                    "report_status": 'null'
                },
                {
                    "idcomment": 337854,
                    "comment": '',
                    "connector": {
                        "id": 2954475,
                        "type": "IEC_62196_T2"
                    },
                    "score": 1,
                    "charged": 'false',
                    "created_at": "2023-01-01T11:34:50+0000",
                    "created_by": {
                        "id": 212903,
                        "username": "OscarVF",
                        "avatar": "https://cfassets.electromaps.com/img/account_150x150.png",
                        "electromaps_uuid": "b77b5361-e2d7-4a06-8b12-10fa4585fa83"
                    },
                    "report_status": "CHARGE_ERROR"
                }
            ]
        }]
    )

    assert res == [
        {
            'place_id': 349444,
            'comment_id': 353292,
            'author': 'ToniGonzalez',
            'text': 'Esto es un p... cachondeo.',
            'publication_date': '2023-02-28T15:42:11+0000',
            'source': 'electromaps'
        },
        {
            'place_id': 349444,
            'comment_id': 337854,
            'author': 'OscarVF',
            'text': '',
            'publication_date': '2023-01-01T11:34:50+0000',
            'source': 'electromaps'
        }
    ]


def test_processing_comments_from_few_places() -> None:
    res = processing_comments(
        [
            {349444:
                [
                    {
                        "idcomment": 353292,
                        "comment": "Esto es un p... cachondeo.",
                        "connector": 'null',
                        "score": 'null',
                        "charged": 'null',
                        "created_at": "2023-02-28T15:42:11+0000",
                        "created_by": {
                            "id": 173202,
                            "username": "ToniGonzalez",
                            "avatar": "https://cfassets.electromaps.com/img/account_150x150.png",
                            "electromaps_uuid": "945f2144-92b6-46f6-acf5-78c58a7ad1c5"
                        },
                        "report_status": 'null'
                    },
                    {
                        "idcomment": 337854,
                        "comment": '',
                        "connector": {
                            "id": 2954475,
                            "type": "IEC_62196_T2"
                        },
                        "score": 1,
                        "charged": 'false',
                        "created_at": "2023-01-01T11:34:50+0000",
                        "created_by": {
                            "id": 212903,
                            "username": "OscarVF",
                            "avatar": "https://cfassets.electromaps.com/img/account_150x150.png",
                            "electromaps_uuid": "b77b5361-e2d7-4a06-8b12-10fa4585fa83"
                        },
                        "report_status": "CHARGE_ERROR"
                    }
                ]
            },

            {277591:
                [
                    {
                        "idcomment": 366892,
                        "comment": 'Good',
                        "connector": {
                            "id": 2735682,
                            "type": "IEC_62196_T2"
                        },
                        "score": 5,
                        "charged": 0,
                        "created_at": "2023-04-02T11:43:27+0000",
                        "created_by": {
                            "id": 334395,
                            "username": "Pedro_hueva",
                            "avatar": "https://cfmedia.electromaps.com/profile_images/5418501c9a4efb0dc185eac95abf3889_"
                                      "l.jpg",
                            "electromaps_uuid": "b0460511-f885-4060-991d-0c9b7499861d"
                        },
                        "report_status": "WORKING"
                    }
                ]
            }
        ]
    )
    assert res == [
        {
            'place_id': 349444,
            'comment_id': 353292,
            'author': 'ToniGonzalez',
            'text': 'Esto es un p... cachondeo.',
            'publication_date': '2023-02-28T15:42:11+0000',
            'source': 'electromaps'
        },
        {
            'place_id': 349444,
            'comment_id': 337854,
            'author': 'OscarVF',
            'text': '',
            'publication_date': '2023-01-01T11:34:50+0000',
            'source': 'electromaps'
        },
        {
            'place_id': 277591,
            'comment_id': 366892,
            'author': 'Pedro_hueva',
            'text': 'Good',
            'publication_date': '2023-04-02T11:43:27+0000',
            'source': 'electromaps'
        }

    ]
