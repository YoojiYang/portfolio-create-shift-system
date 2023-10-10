# 各ポジションの情報
positions_details = {
    "11" :{"name" : "BALCONY"      , "skills_index": 1, "must_have_skills": True},
    "12" :{"name" : "BOX"          , "skills_index": 5, "must_have_skills": True},
    "13" :{"name" : "docomo"       , "skills_index": 9, "must_have_skills": True},
    "14" :{"name" : "Panasonic"    , "skills_index": 9, "must_have_skills": True},
    "15" :{"name" : "DESK"         , "skills_index": 13, "must_have_skills": True},
    "16" :{"name" : "RECEPTION"    , "skills_index": 17, "must_have_skills": True},
    "17" :{"name" : "On the stairs", "skills_index": 21, "must_have_skills": False}, 
    "18" :{"name" : "LOUNGE"       , "skills_index": 23, "must_have_skills": False},
    "19" :{"name" : "ENTRANCE"     , "skills_index": None, "must_have_skills": False},
    "20" :{"name" : "STAND"        , "skills_index": None, "must_have_skills": False},
}

# スキルがないとアサインできないポジション
must_have_skills_positions = [key for key, details in positions_details.items() if details['must_have_skills']]