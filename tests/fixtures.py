import pytest


@pytest.fixture
def sf11meetinginfo():
    return {
        "id": "meetingInformation",
        "title": "Meeting Information",
        "$formkit": "group",
        "children": [
            {
                "key": "activity_type",
                "id": "activity_type",
                "name": "activity_type",
                "label": "$pgettext('activity_type', 'Meeting or Training')",
                "$formkit": "select",
                "placeholder": '$gettext("Please select")',
                "options": [{"value": "1", "label": "Training"}, {"value": "2", "label": "Meeting"}],
            },
            {
                "key": "activity_subtype",
                "id": "activity_subtype",
                "if": "$get(activity_type).value",
                "name": "activity_subtype",
                "label": "$pgettext('activity_type', 'Activity Type')",
                "$formkit": "select",
                "placeholder": '$gettext("Please select")',
                "options": "$getoptions.sf11.activitySubType($get(activity_type).value)",
            },
            {
                "$formkit": "datepicker",
                "name": "date",
                "id": "date",
                "key": "date",
                "label": '$gettext("Date")',
                "format": "DD/MM/YYYY",
                "valueFormat": "DD/MM/YYYY",
                "calendarIcon": "calendar",
                "nextIcon": "angleRight",
                "prevIcon": "angleLeft",
                "_currentDate": "$getCurrentDate",
                "sectionsSchema": {
                    "day": {
                        "children": [
                            "$day.getDate()",
                            {
                                "if": "$attrs._currentDate().day === $day.getDate()",
                                "children": [
                                    {
                                        "if": "$attrs._currentDate().month === $day.getMonth()",
                                        "children": [
                                            {
                                                "$el": "div",
                                                "if": "$attrs._currentDate().year === $day.getFullYear()",
                                                "attrs": {"class": "formkit-day-highlight"},
                                            }
                                        ],
                                    }
                                ],
                            },
                        ]
                    }
                },
            },
        ],
        "icon": "las la-info-circle",
    }


@pytest.fixture
def sf11():
    """
    This is the complete definition for 'SF 11' as at
    Aug 2023

    To recreate this
    >>> from formkit_python_sync.get_schemas import _run_tsx
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(prexix="SF11", delete=False) as o:
    >>>     o.write(json.dumps(_run_tsx()['SF_1_1']))
    >>>     print(o.name)
    """

    return [
        {
            "id": "meetingInformation",
            "title": "Meeting Information",
            "$formkit": "group",
            "children": [
                {
                    "key": "activity_type",
                    "id": "activity_type",
                    "name": "activity_type",
                    "label": "$pgettext('activity_type', 'Meeting or Training')",
                    "$formkit": "select",
                    "placeholder": '$gettext("Please select")',
                    "options": [{"value": "1", "label": "Training"}, {"value": "2", "label": "Meeting"}],
                },
                {
                    "key": "activity_subtype",
                    "id": "activity_subtype",
                    "if": "$get(activity_type).value",
                    "name": "activity_subtype",
                    "label": "$pgettext('activity_type', 'Activity Type')",
                    "$formkit": "select",
                    "placeholder": '$gettext("Please select")',
                    "options": "$getoptions.sf11.activitySubType($get(activity_type).value)",
                },
                {
                    "$formkit": "datepicker",
                    "name": "date",
                    "id": "date",
                    "key": "date",
                    "label": '$gettext("Date")',
                    "format": "DD/MM/YYYY",
                    "valueFormat": "DD/MM/YYYY",
                    "calendarIcon": "calendar",
                    "nextIcon": "angleRight",
                    "prevIcon": "angleLeft",
                    "_currentDate": "$getCurrentDate",
                    "sectionsSchema": {
                        "day": {
                            "children": [
                                "$day.getDate()",
                                {
                                    "if": "$attrs._currentDate().day === $day.getDate()",
                                    "children": [
                                        {
                                            "if": "$attrs._currentDate().month === $day.getMonth()",
                                            "children": [
                                                {
                                                    "$el": "div",
                                                    "if": "$attrs._currentDate().year === $day.getFullYear()",
                                                    "attrs": {"class": "formkit-day-highlight"},
                                                }
                                            ],
                                        }
                                    ],
                                },
                            ]
                        }
                    },
                },
            ],
            "icon": "las la-info-circle",
        },
        {
            "id": "location",
            "title": "Location",
            "$formkit": "group",
            "children": [
                {
                    "$formkit": "select",
                    "id": "district",
                    "name": "district",
                    "key": "district",
                    "label": "$gettext(Municipality)",
                    "options": "$getLocations()",
                },
                {
                    "$formkit": "select",
                    "id": "administrative_post",
                    "name": "administrative_post",
                    "key": "administrative_post",
                    "label": '$gettext("Administrative Post")',
                    "options": "$getLocations($get(district).value)",
                    "if": "$get(district).value && $get(activity_subtype).value !== '20'",
                },
                {
                    "$formkit": "select",
                    "id": "suco",
                    "name": "suco",
                    "key": "suco",
                    "label": "$gettext(Suco)",
                    "options": "$getLocations($get(district).value, $get(administrative_post).value)",
                    "if": "$get(administrative_post).value && $get(activity_subtype).value !== '20' && $get(activity_subtype).value !== '21'",
                },
                {
                    "$formkit": "select",
                    "id": "aldeia",
                    "name": "aldeia",
                    "key": "aldeia",
                    "label": "$gettext(Aldeia)",
                    "options": "$getLocations($get(district).value, $get(administrative_post).value, $get(suco).value)",
                    "if": "$get(suco).value && $get(activity_type).value !== '1' && $get(activity_subtype).value !== '20' && $get(activity_subtype).value !== '21' && $get(activity_subtype).value !== '1' && $get(activity_subtype).value !== '24' && $get(activity_subtype).value !== '4' && $get(activity_subtype).value !== '11' && $get(activity_subtype).value !== '16' && $get(activity_subtype).value !== '17' && $get(activity_subtype).value !== '28'",
                },
            ],
            "icon": "las la-map-marked-alt",
        },
        {
            "id": "participants",
            "title": "Participants",
            "$formkit": "group",
            "children": [
                {
                    "key": "attendance_male",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 40 && $get(activity_subtype).value != 11",
                    "id": "attendance_male",
                    "name": "attendance_male",
                    "label": "$pgettext('partisipants', 'Total participants male')",
                    "validation": "greaterThanOrEqualSum:kpa_male+community_member_male",
                    "validation-messages": {
                        "greaterThanOrEqualSum": '$gettext("The total participants male should be greater than or equal to the sum of Participants Suku Management Team (SMT) - male and Number of community members - male")'
                    },
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "attendance_female",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 11",
                    "id": "attendance_female",
                    "name": "attendance_female",
                    "label": "$pgettext('partisipants', 'Total participants female')",
                    "validation": "greaterThanOrEqualSum:kpa_female+community_member_female",
                    "validation-messages": {
                        "greaterThanOrEqualSum": '$gettext("The total participants female should be greater than or equal to the sum of Participants Suku Management Team (SMT) - female and Number of community members - female")'
                    },
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "kpa_male",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 20 && $get(activity_subtype).value != 21 && $get(activity_subtype).value != 40 && $get(activity_subtype).value != 11",
                    "id": "kpa_male",
                    "name": "kpa_male",
                    "label": "$pgettext('partisipants', 'Participants Suku Management Team (SMT) - male')",
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "kpa_female",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 11 && $get(activity_subtype).value != 20 && $get(activity_subtype).value != 21",
                    "id": "kpa_female",
                    "name": "kpa_female",
                    "label": "$pgettext('partisipants', 'Participants Suku Management Team (SMT) - female')",
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "disable_male",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 40 && $get(activity_subtype).value != 11",
                    "id": "disable_male",
                    "name": "disable_male",
                    "label": "$pgettext('partisipants', 'Number of People with Disability - male')",
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "disable_female",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 11",
                    "id": "disable_female",
                    "name": "disable_female",
                    "label": "$pgettext('partisipants', 'Number of People with Disability - female')",
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "community_member_male",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 20 && $get(activity_subtype).value != 21 && $get(activity_subtype).value != 40 && $get(activity_subtype).value != 11",
                    "id": "community_member_male",
                    "name": "community_member_male",
                    "label": "$pgettext('partisipants', 'Number of community members - male')",
                    "$formkit": "number",
                    "min": 0,
                },
                {
                    "key": "community_member_female",
                    "if": "$get(activity_type).value !== '----' && $get(activity_subtype).value !== '----' && $get(activity_subtype).value != 16 && $get(activity_subtype).value != 11 && $get(activity_subtype).value != 20 && $get(activity_subtype).value != 21",
                    "id": "community_member_female",
                    "name": "community_member_female",
                    "label": "$pgettext('partisipants', 'Number of community members - female')",
                    "$formkit": "number",
                    "min": 0,
                },
            ],
            "icon": "las la-users",
        },
    ]
