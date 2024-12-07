import requests

# manual for now
names = [
    "lebron james", "kobe bryant", "michael jordan", "bill russell", "kevin durant",
    "lamelo ball", "bronny james", "john havlicek", "joe dumars", "isaiah thomas",
    "ryan arcidiacono", "jameson curry", "kareem abdul-jabbar", "shaquille o'neal", "david robinson",
    "kawhi leonard", "magic johnson", "ben simmons", "terry rozier", "isiah thomas",
    "mark eaton", "rudy gobert", "victor wembanyama", "domantas sabonis", "willis reed",
    "stephen curry", "ray allen", "klay thompson", "damian lillard", "draymond green",
    "mike bibby", "glen rice", "allen iverson", "tyrese haliburton", "george mikan",
    "russell westbrook", "james harden", "jimmy butler", "kevin garnett", "charles barkley",
    "karl malone", "moses malone", "dirk nowitzki", "tracy mcgrady", "vince carter",
    "patrick ewing", "steve francis", "paul pierce", "giannis antetokounmpo", "nikola jokić",
    "bob pettit", "tim duncan", "jason kidd", "steve nash", "mark jackson",
    "kevin johnson", "anfernee hardaway", "anthony edwards", "manu ginóbili", "dwyane wade",
    "gary payton", "john stockton", "luka dončić", "jerry west", "dwight howard",
    "tony parker", "trevor ariza", "kevin love", "gradey dick", "serge ibaka",
    "malachi flynn", "terrence ross", "kelly oubre", "rick fox", "robert horry",
    "jamal murray", "gary harris", "elfrid payton", "arron afflalo", "lou williams",
    "jaylen brown", "jayson tatum", "joel embiid", "pau gasol", "marc gasol",
    "deandre jordan", "demar derozan", "demarcus cousins", "hakeem olajuwon", "andre iguodala",
    "hasheem thabeet", "luc longley", "ja morant", "zion williamson", "chris paul",
    "kevin mchale", "scottie pippen", "trae young", "julius erving", "jalen brunson",
    "karl-anthony towns", "goran dragić", "devin booker", "chris bosh", "muggsy bogues",
    "antawn jamison", "guerschon yabusele", "al horford", "nik stauskas", "norman powell",
    "erick dampier", "t.j. warren", "herbert jones", "mark williams", "marvin williams",
    "james wiseman", "anthony bennett", "jj redick", "kyle korver", "pete maravich",
    "carmelo anthony", "nate thurmond", "jarrett allen", "andrew bynum", "jason terry",
    "elgin baylor", "t.j. leaf", "darius garland", "marvin bagley", "bob mcadoo",
    "gilbert arenas", "yao ming", "paul george", "donovan mitchell", "kyle lowry",
    "amar'e stoudemire", "anthony davis", "cj mccollum", "zach randolph", "jalen rose",
    "jabari parker", "hal greer", "malik monk", "bruce brown", "bruce bowen",
    "jamychal green", "norm nixon", "george hill", "larry bird", "larry nance", "wilt chamberlain"
]

url = "http://127.0.0.1:5000/"

# send POST requests
for name in names:
    response = requests.post(url, data={"player": name})
    
    if response.status_code == 200:
        print(f"Successfully sent: {name}")
    else:
        print(f"Failed to send: {name}, Status Code: {response.status_code}")