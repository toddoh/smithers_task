import json
import numpy
import random
import math

def create_timeslot(timeslots):
    days_preset_hourstaken = []
    days_preset_sleep_train_percent = []
    days_preset_focus_train_percent = []
    days_preset_others_train_all = []

    for slot in timeslots:
        days_preset_hourstaken.append(slot['timeslot'])

    for slot in timeslots:
        if slot['timeslot_type'] is "sleep": #sleep timeslots
            days_preset_sleep = slot['timeslot']
            days_preset_sleep_np = []
            for hr in days_preset_sleep:
                arr = []
                if hr > 0:
                    length = int(math.log10(hr))+1
                    
                    if length == 3:
                        nexthr = int(str(int(str(hr)[:1])+1) + str(hr)[1:3])
                        arr = numpy.arange(hr, nexthr, 5).tolist()
                    elif length == 2:
                        nexthr = int("1"+str(hr))
                        arr = numpy.arange(hr, nexthr, 5).tolist()
                    elif length == 4:
                        nexthr = int(str(int(str(hr)[:2])+1) + str(hr)[2:4])
                        arr = numpy.arange(hr, nexthr, 5).tolist()
                else:
                    arr = numpy.arange(hr, hr+60, 5).tolist()

                for i in arr:
                    if int(str(i)[-2:]) < 60:
                        days_preset_sleep_np.append(i)

            
            for hr in days_preset_sleep_np:
                days_preset_sleep_train_percent.append(hr)

        elif slot['timeslot_type'] is "focus": #focus timeslots
            days_preset_focus_train = slot['timeslot']
            for hr in days_preset_focus_train:
                length = int(math.log10(hr))+1
                arr = []
                if length == 3:
                    nexthr = int(str(int(str(hr)[:1])+1) + str(hr)[1:3])
                    arr = numpy.arange(hr, nexthr, 5).tolist()
                elif length == 2:
                    nexthr = int("1"+str(hr))
                    arr = numpy.arange(hr, nexthr, 5).tolist()
                else:
                    nexthr = int(str(int(str(hr)[:2])+1) + str(hr)[2:4])
                    arr = numpy.arange(hr, nexthr, 5).tolist()

                for i in arr:
                    if int(str(i)[-2:]) < 60:
                        days_preset_focus_train_percent.append(i)
        
        else:
            days_preset_others_train = slot['timeslot']
            days_preset_others_train_percent = []
            for hr in days_preset_others_train:
                length = int(math.log10(hr))+1
                arr = []
                if length == 3:
                    nexthr = int(str(int(str(hr)[:1])+1) + str(hr)[1:3])
                    arr = numpy.arange(hr, nexthr, 5).tolist()
                elif length == 2:
                    nexthr = int("1"+str(hr))
                    arr = numpy.arange(hr, nexthr, 5).tolist()
                else:
                    nexthr = int(str(int(str(hr)[:2])+1) + str(hr)[2:4])
                    arr = numpy.arange(hr, nexthr, 5).tolist()

                for i in arr:
                    if int(str(i)[-2:]) < 60:
                        days_preset_others_train_percent.append(int(i))

            days_preset_others_train_dict = dict()
            days_preset_others_train_dict['timeslot_type'] = slot['timeslot_type']
            days_preset_others_train_dict['timeslot'] = days_preset_others_train_percent
            days_preset_others_train_all.append(days_preset_others_train_dict)
            

    days_full24hours = []
    for i in [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300]:
        arr = numpy.arange(i, i+60, 10).tolist()
        for a in arr:
            days_full24hours.append(a)

    days_preset_hourstaken_flat = [item for sublist in days_preset_hourstaken for item in sublist]
    #print(days_full24hours, days_preset_hourstaken_flat)
    days_full24hours_blanktimeslot = set(days_full24hours) - set(days_preset_hourstaken_flat)

    if len(days_full24hours_blanktimeslot) > 0:
        days_preset_blanktimeslot_train_percent = []
        for hr in days_full24hours_blanktimeslot:
            length = int(math.log10(hr))+1
            arr = []
            if length == 3:
                nexthr = int(str(int(str(hr)[:1])+1) + str(hr)[1:3])
                arr = numpy.arange(hr, nexthr, 5).tolist()
            elif length == 2:
                nexthr = int("1"+str(hr))
                arr = numpy.arange(hr, nexthr, 5).tolist()
            else:
                nexthr = int(str(int(str(hr)[:2])+1) + str(hr)[2:4])
                arr = numpy.arange(hr, nexthr, 5).tolist()

            for i in arr:
                if int(str(i)[-2:]) < 60:
                    days_preset_blanktimeslot_train_percent.append(i)

        days_preset_blanktimeslot_train_percent_clean = set(days_preset_blanktimeslot_train_percent) - set(days_preset_focus_train_percent)
        # days_preset_blanktimeslot_train_percent_sorted = sorted(days_preset_blanktimeslot_train_percent_clean, key=lambda e: int(e))
        # print(days_preset_sleep_train_percent, days_preset_focus_train_percent, days_preset_blanktimeslot_train_percent_sorted)
    else:
        days_preset_blanktimeslot_train_percent_clean = []

    return days_preset_sleep_train_percent, days_preset_blanktimeslot_train_percent_clean, days_preset_focus_train_percent, days_preset_others_train_all


timeslot_configuration_generated_all = []

timeslot_configuration_request = [
    {
        "weekslots": [9001],
        "timeslots": [
            {
                "timeslot_type": "sleep",
                "timeslot": [0,100,200,300,400,500],
                "focus": 0
            },
            {
                "timeslot_type": "work",
                "timeslot": [900,1000,1100,1200,1400,1500,1600,1700],
                "focus": 1
            },
            {
                "timeslot_type": "grocery",
                "timeslot": [1800,1900,2000],
                "focus": 1
            },
            {
                "timeslot_type": "focus",
                "timeslot": [2100],
                "focus": 2
            }
        ]
    },
    {
        "weekslots": [9002,9003,9004],
        "timeslots": [
            {
                "timeslot_type": "sleep",
                "timeslot": [0,100,200,300,400,500],
                "focus": 0
            },
            {
                "timeslot_type": "work",
                "timeslot": [900,1000,1100,1200,1400,1500,1600,1700],
                "focus": 1
            },
            {
                "timeslot_type": "focus",
                "timeslot": [600,730,1500,1900,2000],
                "focus": 2
            }
        ]
    },
    {
        "weekslots": [9005],
        "timeslots": [
            {
                "timeslot_type": "sleep",
                "timeslot": [0,100,200,300,400,500],
                "focus": 0
            },
            {
                "timeslot_type": "work",
                "timeslot": [900,1000,1100,1200,1400,1500,1600,1700],
                "focus": 1
            },
            {
                "timeslot_type": "focus",
                "timeslot": [600,730,1900],
                "focus": 2
            }
        ]
    },
    {
        "weekslots": [9006,9000],
        "timeslots": [
            {
                "timeslot_type": "sleep",
                "timeslot": [0,100,200,300,400,500,600,700,800],
                "focus": 0
            },
            {
                "timeslot_type": "church",
                "timeslot": [1100,1200],
                "focus": 1
            },
            {
                "timeslot_type": "focus",
                "timeslot": [1500,1600,1700],
                "focus": 2
            }
        ]
    }
]

timeslot_request_json = timeslot_configuration_request #json.loads(timeslot_configuration_request)
for slotitem in timeslot_request_json:
    timeslots_generated = create_timeslot(slotitem['timeslots'])
    for day in slotitem['weekslots']:
        for slot in timeslots_generated[0]:
            list = dict()
            list['days'] = day
            list['timeslot'] = int(slot)
            list['focus'] = 0
            list['timeslot_type'] = "sleep"
            list['calendar_event_exist'] = 0
            timeslot_configuration_generated_all.append(list)

        for slot in timeslots_generated[1]:
            list = dict()
            list['days'] = day
            list['timeslot'] = int(slot)
            list['focus'] = 1
            list['timeslot_type'] = "none"
            list['calendar_event_exist'] = 0
            timeslot_configuration_generated_all.append(list)

        for slot in timeslots_generated[2]:
            list = dict()
            list['days'] = day
            list['timeslot'] = int(slot)
            list['focus'] = 2
            list['timeslot_type'] = "focus"
            list['calendar_event_exist'] = 0
            timeslot_configuration_generated_all.extend([list] * 10)

        for group in timeslots_generated[3]:
            for item in group['timeslot']:
                list = dict()
                list['days'] = day
                list['timeslot'] = item
                list['focus'] = 1
                list['timeslot_type'] = group['timeslot_type']
                list['calendar_event_exist'] = 0
                timeslot_configuration_generated_all.extend([list] *10)


# print(json.dumps(all))
with open('./timeslot_data.json', 'w') as outfile:
    json.dump(timeslot_configuration_generated_all, outfile)