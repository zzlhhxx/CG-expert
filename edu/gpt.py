import time

from until.sql_tools import mongo_client, mysql_db_conn
# from until.time_tool import saveTime
import re
import pycountry
import json
from urllib.parse import unquote


def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2  # 返回国家的 ISO 3166-1 alpha-2 两位缩写
    return None


def country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_3=country_code)  # 使用 alpha-3 (3字母缩写)
        return country.name if country else "Unknown"
    except Exception as e:
        return f"Error: {e}"


# 1-39
a = [
    {
        "text": "1975 to 1978 | BS (Biochemistry & Genetics) KU Leuven",
        "name": "KU Leuven",
        "college": "",
        "country": "BE",
        "degree": "BS (Biochemistry & Genetics)"
    },
    {
        "text": "B.Eng., East China Institute of Technology (now Nanjing Univ. of Science and Technology), 1983",
        "name": "East China Institute of Technology (now Nanjing Univ. of Science and Technology)",
        "college": "",
        "country": "CN",
        "degree": "B.Eng."
    },
    {
        "text": "Filosofie doktorsexamen i genetik Sveriges lantbruksuniversitet (SLU) 1993",
        "name": "Sveriges lantbruksuniversitet (SLU)",
        "college": "",
        "country": "SE",
        "degree": "Filosofie doktorsexamen i genetik"
    },
    {
        "text": "Bachelor's Degree, Trent, 1975, Physics & Mathematics",
        "name": "Trent",
        "college": "",
        "country": "CA",
        "degree": "Bachelor's Degree"
    },
    {
        "text": "1958 Ph.D. Cornell University",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "DPhil at Oxford University as a Rhodes scholar",
        "name": "Oxford University",
        "college": "",
        "country": "UK",
        "degree": "DPhil"
    },
    {
        "text": "1973-1974 Prescott College Environmental Science",
        "name": "Prescott College",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "1966 Bachelor of Science (Mathematics and Physics), University of Michigan, Ann Arbor, USA;",
        "name": "University of Michigan, Ann Arbor",
        "college": "",
        "country": "US",
        "degree": "Bachelor of Science (Mathematics and Physics)"
    },
    {
        "text": "1984 Master´s Degree Georg August University Göttingen ; Physics",
        "name": "Georg August University Göttingen",
        "college": "",
        "country": "DE",
        "degree": "Master's Degree"
    },
    {
        "text": "1963-1969 University of Vienna, Psychology",
        "name": "University of Vienna",
        "college": "",
        "country": "AT",
        "degree": ""
    },
    {
        "text": "Bachelor of Medicine/Bachelor of Surgery King's College London1983",
        "name": "King's College London",
        "college": "",
        "country": "UK",
        "degree": "Bachelor of Medicine/Bachelor of Surgery"
    },
    {
        "text": "DGM Award (Award of the German Society for Materials Science, 2011);",
        "name": "",
        "college": "",
        "country": "DE",
        "degree": ""
    },
    {
        "text": "1972 AB - Biology Dartmouth College",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "AB - Biology"
    },
    {
        "text": "1992-1996 Ph.D. Program at Princeton University",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Graduate Student 6/71-3/76 Department of Biochemistry School of Medicine University of Oregon Health Sciences Center Portland, OR 97201",
        "name": "University of Oregon Health Sciences Center",
        "college": "Department of Biochemistry, School of Medicine",
        "country": "US",
        "degree": ""
    },
    {
        "text": "MS: Harvard School of Public Health",
        "name": "Harvard School of Public Health",
        "college": "",
        "country": "US",
        "degree": "MS"
    },
    {
        "text": "1987-11-01 to 1989-07-31 University of Warwick Doctor of Philosophy (Ph.D.), Mathematics",
        "name": "University of Warwick",
        "college": "",
        "country": "UK",
        "degree": "Doctor of Philosophy (Ph.D.)"
    },
    {
        "text": "1957-1962 HBS-B, Openbaar Lyceum \"Schoonoord\", Zeist, NL.",
        "name": "Openbaar Lyceum \"Schoonoord\"",
        "college": "",
        "country": "NL",
        "degree": ""
    },
    {
        "text": "Tennessee Technological University: 1987-09-10 to 1989-12-27 | Ph.D. (Mechanical Engineering)",
        "name": "Tennessee Technological University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. (Mechanical Engineering)"
    },
    {
        "text": "BA, Hampshire College, 1977",
        "name": "Hampshire College",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "medical training at the University of Pavia in 1974",
        "name": "University of Pavia",
        "college": "",
        "country": "IT",
        "degree": ""
    },
    {
        "text": "1975 - 1982 M.Sc. (\"Doctoraal\") in Biology University of Utrecht",
        "name": "University of Utrecht",
        "college": "",
        "country": "NL",
        "degree": "M.Sc. (\"Doctoraal\") in Biology"
    },
    {
        "text": "Ph.D. Chemistry, University of Wisconsin (1966)",
        "name": "University of Wisconsin",
        "college": "",
        "country": "US",
        "degree": "Ph.D. Chemistry"
    },
    {
        "text": "Yale University\tBS\t\tBiology-Psychology",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "BS"
    },
    {
        "text": "University of Michigan M. S. 1978",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "M. S."
    },
    {
        "text": "bachelor's degree from Harvard College in 1970",
        "name": "Harvard College",
        "college": "",
        "country": "US",
        "degree": "bachelor's degree"
    },
    {
        "text": "1071-1978 BS - Biochemistry University of Iowa",
        "name": "University of Iowa",
        "college": "",
        "country": "US",
        "degree": "BS - Biochemistry"
    },
    {
        "text": "1961, PhD Physics, University of California, Berkeley",
        "name": "University of California, Berkeley",
        "college": "",
        "country": "US",
        "degree": "PhD Physics"
    },
    {
        "text": "University of Toronto, M.A.Sc. in Aerospace Studies, 1970",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "M.A.Sc. in Aerospace Studies"
    },
    {
        "text": "M.S., Materials Science and Engineering, M.I.T 1974",
        "name": "M.I.T",
        "college": "",
        "country": "US",
        "degree": "M.S., Materials Science and Engineering"
    },
    {
        "text": "1965 - 1968, Psychology, Syracuse University, Ph.D.",
        "name": "Syracuse University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1963 - 1965, Psychology, Syracuse University, M.S.",
        "name": "Syracuse University",
        "college": "",
        "country": "US",
        "degree": "M.S."
    },
    {
        "text": "1958 - 1963, Psychology, City College of New York, B.A.",
        "name": "City College of New York",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "medical degree McMaster University Medical School",
        "name": "McMaster University",
        "college": "Medical School",
        "country": "CA",
        "degree": "medical degree"
    },
    {
        "text": "medical degrees from Indiana University",
        "name": "Indiana University",
        "college": "",
        "country": "US",
        "degree": "medical degrees"
    },
    {
        "text": "2012 D.Univ. (University of York, UK) Hon",
        "name": "University of York",
        "college": "",
        "country": "UK",
        "degree": "D.Univ."
    },
    {
        "text": "KAIST Lecture Award, KAIST, Korea (2019);",
        "name": "KAIST",
        "college": "",
        "country": "KR",
        "degree": ""
    },
    {
        "text": "1970: Master in Medical Sciences, Graduation from Medical School, University of Copenhagen.",
        "name": "University of Copenhagen",
        "college": "Medical School",
        "country": "DK",
        "degree": "Master in Medical Sciences"
    },
    {
        "text": "Ph.D. at Charles University, Czech Republic, in 2001",
        "name": "Charles University",
        "college": "",
        "country": "CZ",
        "degree": "Ph.D."
    },
    {
        "text": "DVM: School of Veterinary Medicine, Addis Ababa University, 1986",
        "name": "Addis Ababa University",
        "college": "School of Veterinary Medicine",
        "country": "ET",
        "degree": "DVM"
    },
    {
        "text": "University of Toronto Bachelor of Science",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "Bachelor of Science"
    }
]
# 40-80
b = [
    {
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "Bachelor of Science",
        "text": "University of Toronto Bachelor of Science"
    },
    {
        "name": "Queen's University",
        "college": "",
        "country": "CA",
        "degree": "B.S. Biological Sciences",
        "text": "B.S. Biological Sciences, Queen's University, 1984"
    },
    {
        "name": "University of Salford",
        "college": "",
        "country": "GB",
        "degree": "B.Sc in Economics with Statistics",
        "text": "University of Salford (England) B.Sc in Economics with Statistics (First class) 1968"
    },
    {
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "AB, Mathematics",
        "text": "AB, 1978, Mathematics, Princeton University"
    },
    {
        "name": "MIT",
        "college": "",
        "country": "US",
        "degree": "Ph.D.",
        "text": "MIT (Ph.D.)."
    },
    {
        "name": "University of California, Los Angeles",
        "college": "",
        "country": "US",
        "degree": "M.P.H.",
        "text": "M.P.H., University of California, Los Angeles, 1983 - 1989"
    },
    {
        "name": "University of Tampere",
        "college": "",
        "country": "FI",
        "degree": "Doctor of Philosophy (Ph.D.), Sports and Exercise",
        "text": "1985-1988 University of Tampere Doctor of Philosophy (Ph.D.), Sports and Exercise"
    },
    {
        "name": "St Bartholomew's Hospital",
        "college": "",
        "country": "GB",
        "degree": "MBBS",
        "text": "St Bartholomew's Hospital: London, GB 1978 to 1980 | MBBS"
    },
    {
        "name": "The Pennsylvania State University",
        "college": "",
        "country": "US",
        "degree": "Ph D, Organizational Strategy and Policy",
        "text": "Ph D, Organizational Strategy and Policy, The Pennsylvania State University, 1979"
    },
    {
        "name": "Madurai University",
        "college": "",
        "country": "IN",
        "degree": "M. S. (Chemistry)",
        "text": "M. S. (Chemistry), Madurai University, Madurai, India, 1976"
    },
    {
        "name": "Madurai University",
        "college": "",
        "country": "IN",
        "degree": "B. S. (Chemistry)",
        "text": "B. S. (Chemistry), Madurai University, Madurai, India, 1974"
    },
    {
        "name": "Harvard College",
        "college": "",
        "country": "US",
        "degree": "B.A. (Social Relations)",
        "text": "Harvard College, 1968. B.A. (Social Relations)"
    },
    {
        "name": "Eberhard-Karls-Universität Tübingen",
        "college": "",
        "country": "DE",
        "degree": "PhD, Toxicology",
        "text": "1981-1983 Eberhard-Karls-Universität Tübingen / University of Tuebingen PhD, Toxicology"
    },
    {
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "PhD",
        "text": "Cornell University PhD -1967"
    },
    {
        "name": "Indian Institute of Technology, Bombay",
        "college": "",
        "country": "IN",
        "degree": "B.S.",
        "text": "B.S. Indian Institute of Technology, Bombay"
    },
]
# 81-100
c = [
    {
        "name": "",
        "college": "",
        "country": "",
        "degree": "BSc & PhD Chemistry",
        "text": "BSc & PhD Chemistry"
    },
    {
        "name": "University of Pennsylvania",
        "college": "",
        "country": "US",
        "degree": "BS, BA",
        "text": "1967-1968 Graduate work, University of Pennsylvania, BS, BA"
    },
    {
        "name": "Northwestern University",
        "college": "",
        "country": "US",
        "degree": "D.Sc.h.c.",
        "text": "D.Sc.h.c., Northwestern University"
    },
    {
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "BA",
        "text": "1964 Biology, Columbia University, BA"
    },
    {
        "name": "University of Innsbruck",
        "college": "",
        "country": "AT",
        "degree": "doctoral degree",
        "text": "doctoral degree in 1994 University of Innsbruck"
    },
    {
        "name": "Chuo University",
        "college": "",
        "country": "JP",
        "degree": "Bachelor of Science",
        "text": "Bachelor of Science from Chuo University in 1986"
    },
    {
        "name": "Universität Basel",
        "college": "",
        "country": "CH",
        "degree": "Dr. h.c. Doctor honoris causa in psychology",
        "text": "Dr. h.c. Doctor honoris causa in psychology, Universität Basel, Switzerland, 2016"
    },
    {
        "name": "University of California, Berkeley",
        "college": "",
        "country": "US",
        "degree": "M.A.",
        "text": "1972-1975 M.A., University of California, Berkeley"
    },
    {
        "name": "University of Pennsylvania",
        "college": "",
        "country": "US",
        "degree": "",
        "text": "attended the University of Pennsylvania"
    },
    {
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Bachelor of Science in Physics",
        "text": "Bachelor of Science in Physics from the Massachusetts Institute of Technology, February 1982"
    },
    {
        "name": "Ohio State University",
        "college": "",
        "country": "US",
        "degree": "Doctor of Philosophy, Metallurgical Engineering",
        "text": "1990 Doctor of Philosophy, Metallurgical Engineering, Ohio State University"
    },
    {
        "name": "KU Leuven",
        "college": "",
        "country": "BE",
        "degree": "Promotion",
        "text": "1985 Promotion at the University KU Leuven"
    },
    {
        "name": "Northwestern University",
        "college": "",
        "country": "US",
        "degree": "Ph.D.",
        "text": "Ph.D. in 1943 from Northwestern University"
    },
    {
        "name": "Johannes Kepler University Linz",
        "college": "",
        "country": "AT",
        "degree": "Dr. tech",
        "text": "1995: Promotion (Dr. tech), Institute of Physical Chemistry, Johannes Kepler University Linz."
    },
    {
        "name": "Touro College",
        "college": "",
        "country": "US",
        "degree": "BA in Psychology",
        "text": "received BA in Psychology from Touro College in 1975."
    },
    {
        "name": "Moscow State University",
        "college": "",
        "country": "RU",
        "degree": "PhD",
        "text": "PhD Moscow State University (1993)"
    },
    {
        "name": "Harvard School of Public Health",
        "college": "",
        "country": "US",
        "degree": "Dr.P.H. (Epidemiology)",
        "text": "1975: Dr.P.H., Harvard School of Public Health (Epidemiology)"
    },
    {
        "name": "Ecole Polytechnique of Paris",
        "college": "",
        "country": "FR",
        "degree": "Engineering Diploma",
        "text": "1981-1984 Engineering Diploma Ecole Polytechnique of Paris"
    },
    {
        "name": "George Washington University",
        "college": "",
        "country": "US",
        "degree": "Statistics",
        "text": "studied Statistics at George Washington University (1976-1977)"
    },
    {
        "name": "Northwestern University",
        "college": "",
        "country": "US",
        "degree": "BS",
        "text": "BS (1983) from Northwestern University"
    }
]
#100-140
d140=[
    {
        "text": "1994 MSc Medical Statistics University of Leicester UK / Leicester",
        "name": "University of Leicester",
        "college": "",
        "country": "UK",
        "degree": "MSc in Medical Statistics"
    },
    {
        "text": "University of California, Berkeley, Mechanical Engineering, Ph.D. 1993",
        "name": "University of California, Berkeley",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Mechanical Engineering"
    },
    {
        "text": "B.Sc. degree with honors in Chemistry from Melbourne University, Australia (1966)",
        "name": "Melbourne University",
        "college": "",
        "country": "AU",
        "degree": "B.Sc. in Chemistry"
    },
    {
        "text": "in 1967 to study osseointegrated implants at Gothenburg University.",
        "name": "Gothenburg University",
        "college": "",
        "country": "SE",
        "degree": ""
    },
    {
        "text": "PhD at University of Helsinki",
        "name": "University of Helsinki",
        "college": "",
        "country": "FI",
        "degree": "Ph.D."
    },
    {
        "text": "University of Glasgow School of Medicine 1987 | MD",
        "name": "University of Glasgow School of Medicine",
        "college": "",
        "country": "GB",
        "degree": "MD"
    },
    {
        "text": "Wayne State University, M.B.A., 1972",
        "name": "Wayne State University",
        "college": "",
        "country": "US",
        "degree": "M.B.A."
    },
    {
        "text": "University of Sydney, PhD in theoretical physics in 1959",
        "name": "University of Sydney",
        "college": "",
        "country": "AU",
        "degree": "Ph.D. in Theoretical Physics"
    },
    {
        "text": "1953 - 1956, Chemistry, Hebrew University of Jerusalem, Ph D",
        "name": "Hebrew University of Jerusalem",
        "college": "",
        "country": "IL",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "Ph.D.(computer science),Massachusetts Institute of Technology,1996",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Computer Science"
    },
    {
        "text": "1961-1965 McGill University Bachelor of Engineering - Chemical",
        "name": "McGill University",
        "college": "",
        "country": "CA",
        "degree": "Bachelor of Engineering - Chemical"
    },
    {
        "text": "1973-1976 University of Oxford Bachelor of Arts (BA), Experimental Psychology",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "Bachelor of Arts (BA) in Experimental Psychology"
    },
    {
        "text": "MD, Stanford University School of Medicine, 1965",
        "name": "Stanford University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "PhD in 1969 at the University of Geneva",
        "name": "University of Geneva",
        "college": "",
        "country": "CH",
        "degree": "Ph.D."
    },
    {
        "text": "medical degree from Guy’s Hospital Medical School at the University of London",
        "name": "Guy’s Hospital Medical School, University of London",
        "college": "",
        "country": "GB",
        "degree": "Medical Degree"
    },
    {
        "text": "medical degree from Harvard Medical School",
        "name": "Harvard Medical School",
        "college": "",
        "country": "US",
        "degree": "Medical Degree"
    },
    {
        "text": "M.D., 1982 Tufts University School of Medicine",
        "name": "Tufts University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "Ph.D., University of Michigan, 1976",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1996-2002 Mayo Clinic Graduate School of Biomedical Sciences Master of Science (MS) / Doctor of Philosophy (PhD), Clinical Research / Biomedical Engineering",
        "name": "Mayo Clinic Graduate School of Biomedical Sciences",
        "college": "",
        "country": "US",
        "degree": "MS / Ph.D. in Clinical Research / Biomedical Engineering"
    },
    {
        "text": "1975-1980 Scotch College, Melbourne Doctor of Philosophy (Ph.D.), Immunology",
        "name": "Scotch College, Melbourne",
        "college": "",
        "country": "AU",
        "degree": "Ph.D. in Immunology"
    },
    {
        "text": "Ph.D. Marine Sciences, McGill University, Montreal, Canada, 1973",
        "name": "McGill University",
        "college": "",
        "country": "CA",
        "degree": "Ph.D. in Marine Sciences"
    },
    {
        "text": "DMD, Dental Medicine, Harvard School of Dental Medicine",
        "name": "Harvard School of Dental Medicine",
        "college": "",
        "country": "US",
        "degree": "DMD in Dental Medicine"
    },
    {
        "text": "B.S. in chemistry, 1972 University of Illinois, Champaign-Urbana",
        "name": "University of Illinois, Champaign-Urbana",
        "college": "",
        "country": "US",
        "degree": "B.S. in Chemistry"
    },
    {
        "text": "1972 Medical School American University of Beirut",
        "name": "American University of Beirut",
        "college": "",
        "country": "LB",
        "degree": "Medical Degree"
    },
    {
        "text": "Dartmouth College, Hanover, NH, BA, 1968",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "MD U.S. Army Biomedical Research Laboratory",
        "name": "U.S. Army Biomedical Research Laboratory",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "BS 1965-1969",
        "name": "",
        "college": "",
        "country": "",
        "degree": "BS"
    },
    {
        "text": "Ph.D., Economics, UCLA, 1987.",
        "name": "UCLA",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Economics"
    },
    {
        "text": "A.B., Economics, Cornell University, Phi Beta Kappa, 1982.",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "A.B. in Economics"
    },
    {
        "text": "University of Toronto Faculty of Medicine, MD",
        "name": "University of Toronto Faculty of Medicine",
        "college": "",
        "country": "CA",
        "degree": "MD"
    },
    {
        "text": "1992, Ph.D. ECE, University of Illinois at Urbana-Champaign",
        "name": "University of Illinois at Urbana-Champaign",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in ECE"
    },
    {
        "text": "MA Biochemistry, Oxford University (UK), 1971",
        "name": "Oxford University",
        "college": "",
        "country": "GB",
        "degree": "MA in Biochemistry"
    },
    {
        "text": "Ph.D., University of Michigan, 1967",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "University of California Berkeley: Berkeley, CA, US",
        "name": "University of California Berkeley",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "MSc, Harvard School of Public Health 1995-1997",
        "name": "Harvard School of Public Health",
        "college": "",
        "country": "US",
        "degree": "MSc"
    },
    {
        "text": "Virginia Commonwealth University, USA, Chemistry Diploma",
        "name": "Virginia Commonwealth University",
        "college": "",
        "country": "US",
        "degree": "Chemistry Diploma"
    },
    {
        "text": "A.M., Economics, May 1989, Brown University, Providence",
        "name": "Brown University",
        "college": "",
        "country": "US",
        "degree": "A.M. in Economics"
    },
    {
        "text": "PhD, 1971, Massachusetts Institute of Technology",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Ph.D. in cell biology at the Biocenter of the University of Basel in 1984",
        "name": "University of Basel",
        "college": "Biocenter",
        "country": "CH",
        "degree": "Ph.D. in Cell Biology"
    },
    {
        "text": "University College London (PhD) 1978",
        "name": "University College London",
        "college": "",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "MD, The Johns Hopkins University School of Medicine, 1989",
        "name": "The Johns Hopkins University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    }
]
#141-180
d180=[
    {
        "text": "University of Cambridge Medicine: Cambridge, Cambridgeshire, GB 1980 to 1983 | MA Cantab",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "MA Cantab in Medicine"
    },
    {
        "text": "Iowa State University MS 1981 Economics",
        "name": "Iowa State University",
        "college": "",
        "country": "US",
        "degree": "MS in Economics"
    },
    {
        "text": "Honorary Professor, Katholieke Universiteit Leuven, Belgium (2014);",
        "name": "Katholieke Universiteit Leuven",
        "college": "",
        "country": "BE",
        "degree": ""
    },
    {
        "text": "MA, MBBChir, University of Cambridge",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "MA, MBBChir"
    },
    {
        "text": "1986-1991 University of Wisconsin-Madison PhD, Microbiology and Immunology",
        "name": "University of Wisconsin-Madison",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Microbiology and Immunology"
    },
    {
        "text": "Wesleyan University Connecticut M.A, 1964 Analytical Chemistry",
        "name": "Wesleyan University",
        "college": "",
        "country": "US",
        "degree": "M.A. in Analytical Chemistry"
    },
    {
        "text": "Richard C. Larock, Distinguished Professor Emeritus of Chemistry, received his Ph.D. from Purdue University in 1972, after completing his undergraduate training at the University of California, Davis, in 1967.",
        "name": "Purdue University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "1972 B.Sc St. Xavier’s College, Bombay",
        "name": "St. Xavier’s College",
        "college": "",
        "country": "IN",
        "degree": "B.Sc."
    },
    {
        "text": "University of Pavia : Pavia , IT",
        "name": "University of Pavia",
        "college": "",
        "country": "IT",
        "degree": ""
    },
    {
        "text": "1979 to 1985 , M.D. Summa cum laude",
        "name": "",
        "college": "",
        "country": "",
        "degree": "M.D. Summa cum laude"
    },
    {
        "text": "1964-10-01 to 1965-11-01 | Diploma in Abnormal Psychology (Institute of Psychiatry), University Of London",
        "name": "University Of London",
        "college": "Institute of Psychiatry",
        "country": "GB",
        "degree": "Diploma in Abnormal Psychology"
    },
    {
        "text": "undergraduate student at St. Francis Xavier University in Nova Scotia",
        "name": "St. Francis Xavier University",
        "college": "",
        "country": "CA",
        "degree": ""
    },
    {
        "text": "Washington University School of Medicine in St. Louis (M.D., 1955)",
        "name": "Washington University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "1985 – 1988",
        "name": "",
        "college": "",
        "country": "",
        "degree": ""
    },
    {
        "text": "1967 Ph.D. in Biophysics, Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biophysics"
    },
    {
        "text": "Licenciado en Fisica. Instituto Balseiro, Bariloche, Argentina (1982)",
        "name": "Instituto Balseiro",
        "college": "",
        "country": "AR",
        "degree": "Licenciado en Fisica"
    },
    {
        "text": "1994-06-01 | BSc (Hons) Biochemistry/Immunology (Department of Biochemistry) University of Aberdeen",
        "name": "University of Aberdeen",
        "college": "Department of Biochemistry",
        "country": "GB",
        "degree": "BSc (Hons) in Biochemistry/Immunology"
    },
    {
        "text": "A. B. Princeton University, 1967-1970",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "A.B."
    },
    {
        "text": "BSc, Electrical Engineering, Queen's University, 1953",
        "name": "Queen's University",
        "college": "",
        "country": "CA",
        "degree": "BSc in Electrical Engineering"
    },
    {
        "text": "MSc, Electrical Engineering, Queen's University, 1961",
        "name": "Queen's University",
        "college": "",
        "country": "CA",
        "degree": "MSc in Electrical Engineering"
    },
    {
        "text": "PhD, Physiology & Biophysics, Dalhousie University, 1967",
        "name": "Dalhousie University",
        "college": "",
        "country": "CA",
        "degree": "Ph.D. in Physiology & Biophysics"
    },
    {
        "text": "Epidemiology ScM at Harvard School of Public Health",
        "name": "Harvard School of Public Health",
        "college": "",
        "country": "US",
        "degree": "ScM in Epidemiology"
    },
    {
        "text": "BS, Engineering Mechanics, September 1981 - July 1985, Xi'an Jiaotong University.",
        "name": "Xi'an Jiaotong University",
        "college": "",
        "country": "CN",
        "degree": "BS in Engineering Mechanics"
    },
    {
        "text": "1975 Docent in Biochemistry, University of Helsinki, Finland",
        "name": "University of Helsinki",
        "college": "",
        "country": "FI",
        "degree": "Docent in Biochemistry"
    },
    {
        "text": "1986 Ph.D., Electrical Engineering, Stanford University, Stanford, California",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Electrical Engineering"
    },
    {
        "text": "MSc in epidemiology from LSHTM in 1981",
        "name": "LSHTM",
        "college": "",
        "country": "GB",
        "degree": "MSc in Epidemiology"
    },
    {
        "text": "1973 PhD in Medicine, University of Helsinki, Finland",
        "name": "University of Helsinki",
        "college": "",
        "country": "FI",
        "degree": "Ph.D. in Medicine"
    },
    {
        "text": "Sep 1959 - Jun 1965 University of Pennsylvania (M.A.) (1936)",
        "name": "University of Pennsylvania",
        "college": "",
        "country": "US",
        "degree": "M.A."
    },
    {
        "text": "1997 Promotion at University of Konstanz",
        "name": "University of Konstanz",
        "college": "",
        "country": "DE",
        "degree": ""
    },
    {
        "text": "Diploma, Computer Science & Mathematics, 1983 – 1987 Technical University of Munich",
        "name": "Technical University of Munich",
        "college": "",
        "country": "DE",
        "degree": "Diploma in Computer Science & Mathematics"
    },
    {
        "text": "1993-10-01 to 1997-05-01 | PhD (Department of Community Medicine)",
        "name": "Department of Community Medicine",
        "college": "",
        "country": "",
        "degree": "Ph.D."
    },
    {
        "text": "1978-1981 BSc (1st Class Honours),University of York, UK",
        "name": "University of York",
        "college": "",
        "country": "GB",
        "degree": "BSc (1st Class Honours)"
    },
    {
        "text": "master’s degrees from Indiana University",
        "name": "Indiana University",
        "college": "",
        "country": "US",
        "degree": "Master’s Degrees"
    },
    {
        "text": "04/2003-03/2005......Tokyo Institute of Technology, Japan (MSc)",
        "name": "Tokyo Institute of Technology",
        "college": "",
        "country": "JP",
        "degree": "MSc"
    },
    {
        "text": "1989 B.S., University of Rochester, Physics (1970)",
        "name": "University of Rochester",
        "college": "",
        "country": "US",
        "degree": "B.S. in Physics"
    },
    {
        "text": "M.D., Dept. of Chemistry, Karolinska Institute",
        "name": "Karolinska Institute",
        "college": "Dept. of Chemistry",
        "country": "SE",
        "degree": "M.D."
    },
    {
        "text": "BSc from the Pukyong National University",
        "name": "Pukyong National University",
        "college": "",
        "country": "KR",
        "degree": "BSc"
    },
    {
        "text": "In 1994 doctorate degree University of Sussex",
        "name": "University of Sussex",
        "college": "",
        "country": "GB",
        "degree": "Doctorate Degree"
    },
    {
        "text": "MPhil, Computer Science, Yale University, 1982 to 1984",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "MPhil in Computer Science"
    },
    {
        "text": "Doctor of Philosophy (1969) University of Massachusetts, Amherst.",
        "name": "University of Massachusetts, Amherst",
        "college": "",
        "country": "US",
        "degree": "Doctor of Philosophy"
    },
    {
        "text": "1994-07-01 to present, MD (Medicine and Surgery) Monash University: Clayton, VIC, AU",
        "name": "Monash University",
        "college": "",
        "country": "AU",
        "degree": "MD in Medicine and Surgery"
    }
]
#181-200
d200=[
    {
        "text": "undergraduate degree from the University of Berlin in 1967",
        "name": "University of Berlin",
        "college": "",
        "country": "DE",
        "degree": "Undergraduate Degree"
    },
    {
        "text": "Jul 1990 Yale University Master's degree, Liberal Arts and Sciences/Liberal Studies",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "Master's degree in Liberal Arts and Sciences/Liberal Studies"
    },
    {
        "text": "B. S. 1967 to 1969 University of Lucknow, Lucknow, India Physics & Statistics",
        "name": "University of Lucknow",
        "college": "",
        "country": "IN",
        "degree": "B.S. in Physics & Statistics"
    },
    {
        "text": "1971 , B.S. (Chemistry)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "B.S. in Chemistry"
    },
    {
        "text": "MD, University of Missouri-Columbia Columbia, MO (1979)",
        "name": "University of Missouri-Columbia",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "May 1993 - Dec. 1995 Doctor of Philosophy (Ph.D.) in Chemical Engineering received at the University of Birmingham in the United Kingdom",
        "name": "University of Birmingham",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Chemical Engineering"
    },
    {
        "text": "1973 M.Sc. Biochemistry (cum laude)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "M.Sc. in Biochemistry (cum laude)"
    },
    {
        "text": "1972 to 1976 Ph.D., Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "B.B.A. University of Iowa, December 1985",
        "name": "University of Iowa",
        "college": "",
        "country": "US",
        "degree": "B.B.A."
    },
    {
        "text": "1989 Dr. Scient.",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Dr. Scient."
    },
    {
        "text": "B.Eng. Xi'an Jiaotong University",
        "name": "Xi'an Jiaotong University",
        "college": "",
        "country": "CN",
        "degree": "B.Eng."
    },
    {
        "text": "Undergraduate studies at Princeton University in 1978",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "Undergraduate Studies"
    },
    {
        "text": "M.D. New York University School of Medicine 1994",
        "name": "New York University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "B.A. degree at the University of Cambridge",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "B.A."
    },
    {
        "text": "1971-1975 First four years of Medical School completed (University of Uppsala)",
        "name": "University of Uppsala",
        "college": "",
        "country": "SE",
        "degree": "Medical School"
    },
    {
        "text": "1958-1961 B.A. (magna cum laude), History and Economics, Yale University, New Haven, CT",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "B.A. in History and Economics (magna cum laude)"
    },
    {
        "text": "Clarkson University (Potsdam, NY) B.S. in Chemistry (June, 1971)",
        "name": "Clarkson University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Chemistry"
    },
    {
        "text": "Bachelor of Arts University of Cambridge1980",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "Bachelor of Arts"
    },
    {
        "text": "1976-1976 University of Lille 1 Sciences and Technology Summer Course in French",
        "name": "University of Lille 1 Sciences and Technology",
        "college": "",
        "country": "FR",
        "degree": "Summer Course in French"
    },
    {
        "text": "1961-1965 College of the Holy Cross A.B., Philosophy & French",
        "name": "College of the Holy Cross",
        "college": "",
        "country": "US",
        "degree": "A.B. in Philosophy & French"
    }
]
#201-250
d250=[
    {
        "text": "PhD Drexel University (1989)",
        "name": "Drexel University",
        "college": "",
        "country": "US",
        "degree": "PhD"
    },
    {
        "text": "1994-1996 University of Otago Bachelor's degree, Biochemistry",
        "name": "University of Otago",
        "college": "",
        "country": "NZ",
        "degree": "Bachelor's degree in Biochemistry"
    },
    {
        "text": "Ph.D. Bio-Environmental Engineering University of Nebraska, Lincoln, 1979 to 1982",
        "name": "University of Nebraska, Lincoln",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Bio-Environmental Engineering"
    },
    {
        "text": "1992-1996 Massachusetts Institute of Technology Ph.D.",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "B.A., New College of the University South Florida",
        "name": "New College of the University South Florida",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "D. Engineering, Kyoto University, Japan, 1963.",
        "name": "Kyoto University",
        "college": "",
        "country": "JP",
        "degree": "D. Engineering"
    },
    {
        "text": "1984-1989 Harvard University AB, physics",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "AB in Physics"
    },
    {
        "text": "University of Buffalo M.A. 1952 Romance Languages",
        "name": "University of Buffalo",
        "college": "",
        "country": "US",
        "degree": "M.A. in Romance Languages"
    },
    {
        "text": "PhD in theoretical and mathematical physics in 1975 Landau Institute for Theoretical Physics of the USSR (now Russian) Academy of Sciences, Moscow - Chernogolovka",
        "name": "Landau Institute for Theoretical Physics of the USSR",
        "college": "",
        "country": "RU",
        "degree": "PhD in Theoretical and Mathematical Physics"
    },
    {
        "text": "1968-1976 University of Wisconsin, Madison WI Doctor of Medicine (M.D.), Endocrinology",
        "name": "University of Wisconsin, Madison",
        "college": "",
        "country": "US",
        "degree": "M.D. in Endocrinology"
    },
    {
        "text": "Dartmouth College A.B. - 1965",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "A.B."
    },
    {
        "text": "Ph. D. Bristol University, England 1958",
        "name": "Bristol University",
        "college": "",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "6/1981-6/1987 Ph.D. University of Miami School of Medicine in Biochemistry",
        "name": "University of Miami School of Medicine",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "Medical School 1977 MD University of Chicago",
        "name": "University of Chicago",
        "college": "Medical School",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "1982-1984 University of Arizona PhD, Soil and Water Science, Remote Sensing",
        "name": "University of Arizona",
        "college": "",
        "country": "US",
        "degree": "PhD in Soil and Water Science, Remote Sensing"
    },
    {
        "text": "educated in chemistry at the University of Sheffield Ph.D.",
        "name": "University of Sheffield",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "B.Sc. North Dakota State University, 1962",
        "name": "North Dakota State University",
        "college": "",
        "country": "US",
        "degree": "B.Sc."
    },
    {
        "text": "D. Phil. Oxford University, 1966",
        "name": "Oxford University",
        "college": "",
        "country": "GB",
        "degree": "D. Phil."
    },
    {
        "text": "D.Sc. (Honorary) North Dakota State University, 1978",
        "name": "North Dakota State University",
        "college": "",
        "country": "US",
        "degree": "D.Sc. (Honorary)"
    },
    {
        "text": "1985 M.D. University of Buenos Aires, Argentina",
        "name": "University of Buenos Aires",
        "college": "",
        "country": "AR",
        "degree": "M.D."
    },
    {
        "text": "1991 M.P.H. The Johns Hopkins University, School of Hygiene and Public Health",
        "name": "The Johns Hopkins University",
        "college": "School of Hygiene and Public Health",
        "country": "US",
        "degree": "M.P.H."
    },
    {
        "text": "1995 Ph.D. The Johns Hopkins University, School of Hygiene and Public Health, Department of Health Policy and Management",
        "name": "The Johns Hopkins University",
        "college": "School of Hygiene and Public Health, Department of Health Policy and Management",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "August 1976: Ph.D. in EECS , Princeton University",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in EECS"
    },
    {
        "text": "PhD at the University of Paris",
        "name": "University of Paris",
        "college": "",
        "country": "FR",
        "degree": "Ph.D."
    },
    {
        "text": "PhD in psychology at the University of Michigan",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Psychology"
    },
    {
        "text": "Sep 1971-Jun 1974 Vassar College Psychology",
        "name": "Vassar College",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "1985 -- Diploma in Physics, LMU Munich",
        "name": "LMU Munich",
        "college": "",
        "country": "DE",
        "degree": "Diploma in Physics"
    },
    {
        "text": "BS, Industrial Engineering with Computer Science minor, Wayne State University 1980",
        "name": "Wayne State University",
        "college": "",
        "country": "US",
        "degree": "BS in Industrial Engineering with Computer Science minor"
    },
    {
        "text": "B.A., University of Pennsylvania, 1972 - 1976",
        "name": "University of Pennsylvania",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1972 PhD Sociology, Cambridge",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Sociology"
    },
    {
        "text": "1980: M.A. in Clinical Psychology, University of Illinois at Chicago.",
        "name": "University of Illinois at Chicago",
        "college": "",
        "country": "US",
        "degree": "M.A. in Clinical Psychology"
    }
]
#251-280
d280=[
    {
        "text": "University of Bristol Doctor of Philosophy (Ph.D.), Biochemistry 1965 - 1968",
        "name": "University of Bristol",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "Jesus College, Cambridge Master of Arts (M.A.), Biochemistry 1962 - 1965",
        "name": "Jesus College, Cambridge",
        "college": "",
        "country": "GB",
        "degree": "M.A. in Biochemistry"
    },
    {
        "text": "B.Sc. American University In Cairo, Cairo, Egypt Feb. 1977",
        "name": "American University In Cairo",
        "college": "",
        "country": "EG",
        "degree": "B.Sc."
    },
    {
        "text": "MPhil, Institute of Psychiatry, University of Oxford",
        "name": "University of Oxford",
        "college": "Institute of Psychiatry",
        "country": "GB",
        "degree": "MPhil"
    },
    {
        "text": "University of California, Berkeley, Biochemistry, Ph.D., 1966-1967",
        "name": "University of California, Berkeley",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "1997 , Ph.D Michigan State University",
        "name": "Michigan State University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1981-1988 Seoul National University, Chemical Education, BS",
        "name": "Seoul National University",
        "college": "",
        "country": "KR",
        "degree": "BS in Chemical Education"
    },
    {
        "text": "B. Tech., Electrical Engineering, Indian Institute of Technology, Kanpur 1969",
        "name": "Indian Institute of Technology, Kanpur",
        "college": "",
        "country": "IN",
        "degree": "B. Tech. in Electrical Engineering"
    },
    {
        "text": "PhD in Biological Sciences at the University of Siena",
        "name": "University of Siena",
        "college": "",
        "country": "IT",
        "degree": "Ph.D. in Biological Sciences"
    },
    {
        "text": "1972: BA, Zoology, Oxford, U.K.",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "BA in Zoology"
    },
    {
        "text": "1969 Ph.D., University of Vienna, (Psychology)",
        "name": "University of Vienna",
        "college": "",
        "country": "AT",
        "degree": "Ph.D. in Psychology"
    },
    {
        "text": "B.A. in Biology, Swarthmore College l966",
        "name": "Swarthmore College",
        "college": "",
        "country": "US",
        "degree": "B.A. in Biology"
    },
    {
        "text": "Master of Science Harbin Medical School - 1985",
        "name": "Harbin Medical School",
        "college": "",
        "country": "CN",
        "degree": "Master of Science"
    },
    {
        "text": "Cornell University Medical College (M.D., 1956)",
        "name": "Cornell University Medical College",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "1982 MD - MIT Program in Health Sciences and Technology Harvard Medical School",
        "name": "Harvard Medical School",
        "college": "MIT Program in Health Sciences and Technology",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "1998-2002 Ph.D, Chemistry, Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "The Rockefeller University",
        "name": "The Rockefeller University",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "1982-1991 University of Amsterdam MD, Medicine",
        "name": "University of Amsterdam",
        "college": "",
        "country": "NL",
        "degree": "MD in Medicine"
    },
    {
        "text": "B.S., U.P. Agricultural University – India, Engineering and Technology, Sep 1967",
        "name": "U.P. Agricultural University",
        "college": "",
        "country": "IN",
        "degree": "B.S. in Engineering and Technology"
    },
    {
        "text": "Ph.D. in economics from Yale University in 1985",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Economics"
    },
    {
        "text": "1982 Specialization in Neurology (Board Certification), University of Pavia, Pavia, Italy",
        "name": "University of Pavia",
        "college": "",
        "country": "IT",
        "degree": "Specialization in Neurology"
    },
    {
        "text": "1980 Ph.D. in Clinical Pharmacology, University of London, London, U.K",
        "name": "University of London",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Clinical Pharmacology"
    },
    {
        "text": "1975 M.D. Degree, with honours, University of Pavia, Pavia, Italy",
        "name": "University of Pavia",
        "college": "",
        "country": "IT",
        "degree": "M.D. Degree"
    },
    {
        "text": "Nov-1986, Kindai University, Degree, Doctor of Medicine",
        "name": "Kindai University",
        "college": "",
        "country": "JP",
        "degree": "Doctor of Medicine"
    },
    {
        "text": "1992-09 to 1995-06, MS (Chemistry) Nanjing University",
        "name": "Nanjing University",
        "college": "",
        "country": "CN",
        "degree": "MS in Chemistry"
    },
    {
        "text": "1978 Diploma (MSc) in Sociology, University of Marburg",
        "name": "University of Marburg",
        "college": "",
        "country": "DE",
        "degree": "Diploma (MSc) in Sociology"
    },
    {
        "text": "BA from New York University",
        "name": "New York University",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "2004-08-01 to 2008-08-01 PhD in machine learning from Carnegie Mellon University",
        "name": "Carnegie Mellon University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Machine Learning"
    },
    {
        "text": "1976 University degree, Geneva University of Applied Sciences, CH",
        "name": "Geneva University of Applied Sciences",
        "college": "",
        "country": "CH",
        "degree": "University Degree"
    },
    {
        "text": "Presidency College, Calcutta (B.A. 1953)",
        "name": "Presidency College, Calcutta",
        "college": "",
        "country": "IN",
        "degree": "B.A."
    }
]
#281-320
d320=[
    {
        "text": "Butler University, Indianapolis, Indiana Chemistry, cum laude BS",
        "name": "Butler University",
        "college": "",
        "country": "US",
        "degree": "BS in Chemistry (cum laude)"
    },
    {
        "text": "B.S. Stanford University 1970-1974",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "1962-1967 \"Licenciaat\" (Master) in Medical Sciences, Katholieke Universiteit Leuven, Belgium. Summa cum laude.",
        "name": "Katholieke Universiteit Leuven",
        "college": "",
        "country": "BE",
        "degree": "Master in Medical Sciences"
    },
    {
        "text": "MD, Faculty of Medicine Barcelona Univ",
        "name": "Faculty of Medicine Barcelona Univ",
        "college": "",
        "country": "ES",
        "degree": "MD"
    },
    {
        "text": "Massachusetts Institute of Technology, Ph. D in Physics, 1997.",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Physics"
    },
    {
        "text": "BA Cornell University 1972 to 1976",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "1996-06-20 Ph.D. University Of Tartu, Estonia.",
        "name": "University Of Tartu",
        "college": "",
        "country": "EE",
        "degree": "Ph.D."
    },
    {
        "text": "Master of Science degree, physiology of transport & secretion (1956), McGill University",
        "name": "McGill University",
        "college": "",
        "country": "CA",
        "degree": "Master of Science in Physiology of Transport & Secretion"
    },
    {
        "text": "University of British Columbia, 1978",
        "name": "University of British Columbia",
        "college": "",
        "country": "CA",
        "degree": ""
    },
    {
        "text": "1979 American University of Beirut, Beirut, LBN, MD, Medicine",
        "name": "American University of Beirut",
        "college": "",
        "country": "LB",
        "degree": "MD in Medicine"
    },
    {
        "text": "1989 B.S. in Psychology, University of Oregon (Summa Cum Laude)",
        "name": "University of Oregon",
        "college": "",
        "country": "US",
        "degree": "B.S. in Psychology"
    },
    {
        "text": "University of Michigan, Ph.D, 1967",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1965-1968, Tohoku University, Sendai, Majoring in Physics; Ph.D",
        "name": "Tohoku University",
        "college": "",
        "country": "JP",
        "degree": "Ph.D. in Physics"
    },
    {
        "text": "Universität des Saarlandes: Saarbrucken, Saarland, DE 1961-10-01 to 1965-06-01 | Vordiplom in Experimental Psycholgoy",
        "name": "Universität des Saarlandes",
        "college": "",
        "country": "DE",
        "degree": "Vordiplom in Experimental Psychology"
    },
    {
        "text": "1973 : DEA de Physique Th´eorique, option Relativit´e et Th´eorie des Champs",
        "name": "",
        "college": "",
        "country": "",
        "degree": "DEA in Theoretical Physics, Relativity, and Field Theory"
    },
    {
        "text": "Ph.D., Operational Research, London School of Economics (advisor: Ailsa H. Land) 1972-1975",
        "name": "London School of Economics",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Operational Research"
    },
    {
        "text": "1982: Ph.D. in Clinical Psychology. University of Illinois at Chicago.",
        "name": "University of Illinois at Chicago",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Clinical Psychology"
    },
    {
        "text": "undergraduate (B.S., 1967) at the Massachusetts Institute of Technology",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "B.A. 1960-1965 City University of New York, Hunter College",
        "name": "City University of New York, Hunter College",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "2010-2016 Member, Council of Science and Humanities of the German Government (Wissenschaftsrat)",
        "name": "",
        "college": "",
        "country": "DE",
        "degree": ""
    },
    {
        "text": "Dipl. Eng., National Technical University of Athens, Greece (1966-1971)",
        "name": "National Technical University of Athens",
        "college": "",
        "country": "GR",
        "degree": "Dipl. Eng."
    },
    {
        "text": "1970 BS Faculty of Engineering, Kyoto University",
        "name": "Kyoto University",
        "college": "Faculty of Engineering",
        "country": "JP",
        "degree": "BS"
    },
    {
        "text": "MSc in Biology from Aarhus University 1973",
        "name": "Aarhus University",
        "college": "",
        "country": "DK",
        "degree": "MSc in Biology"
    },
    {
        "text": "Bachelor of Science degree from Baylor University in 1984",
        "name": "Baylor University",
        "college": "",
        "country": "US",
        "degree": "Bachelor of Science"
    },
    {
        "text": "1996-1998 Indian Institute of Technology, Bombay Master of Science, Applied Geology",
        "name": "Indian Institute of Technology, Bombay",
        "college": "",
        "country": "IN",
        "degree": "Master of Science in Applied Geology"
    },
    {
        "text": "1995 Boston University, B.A. (Psychology)",
        "name": "Boston University",
        "college": "",
        "country": "US",
        "degree": "B.A. in Psychology"
    },
    {
        "text": "MSc (Chem. Eng.) National Taiwan University, 1973 to 1977",
        "name": "National Taiwan University",
        "college": "",
        "country": "TW",
        "degree": "MSc in Chemical Engineering"
    },
    {
        "text": "MSChem and PhD in Chemical Physics, 1961",
        "name": "",
        "college": "",
        "country": "",
        "degree": "MSChem and PhD in Chemical Physics"
    },
    {
        "text": "A.B. at Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "A.B."
    },
    {
        "text": "B.A., West Virginia Wesleyan College 1976",
        "name": "West Virginia Wesleyan College",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1977-09-01 to 1980-09-01 , D.Phil. (Sir William Dunn School of Pathology) University of Oxford",
        "name": "University of Oxford",
        "college": "Sir William Dunn School of Pathology",
        "country": "GB",
        "degree": "D.Phil."
    },
    {
        "text": "University of Chicago, Ph.D., Chemistry, 1995",
        "name": "University of Chicago",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "Bachelor of Arts, University of Oxford 1971",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "Bachelor of Arts"
    },
    {
        "text": "PhD Belgrade University (1969)",
        "name": "Belgrade University",
        "college": "",
        "country": "RS",
        "degree": "PhD"
    },
    {
        "text": "MSc Hebrew University of Jerusalem (1969)",
        "name": "Hebrew University of Jerusalem",
        "college": "",
        "country": "IL",
        "degree": "MSc"
    },
    {
        "text": "Ph.D. in neurobiology and behavior at Cornell University Graduate School",
        "name": "Cornell University Graduate School",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Neurobiology and Behavior"
    },
    {
        "text": "State University of New York at Stony Brook M.S., Computer Science 1972",
        "name": "State University of New York at Stony Brook",
        "college": "",
        "country": "US",
        "degree": "M.S. in Computer Science"
    },
    {
        "text": "M.S. in biochemistry in 1993 from the University of Tübingen, Germany",
        "name": "University of Tübingen",
        "college": "",
        "country": "DE",
        "degree": "M.S. in Biochemistry"
    },
    {
        "text": "In 1998, Ph.D. in microbiology from the University of Tübingen, Germany",
        "name": "University of Tübingen",
        "college": "",
        "country": "DE",
        "degree": "Ph.D. in Microbiology"
    },
    {
        "text": "PhD, Personality at the University of Michigan, 1963",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Personality"
    },
    {
        "text": "M.A. in Physics in 1975 from Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "M.A. in Physics"
    }
]
#321-360
d360=[
    {
        "text": "PhD, 1971 Molecular Biology, Vanderbilt University",
        "name": "Vanderbilt University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Molecular Biology"
    },
    {
        "text": "BEd, Liverpool & Lancaster Universities, 1974",
        "name": "Liverpool & Lancaster Universities",
        "college": "",
        "country": "GB",
        "degree": "B.Ed."
    },
    {
        "text": "M.Sc. (1971) Hebrew University in Jerusalem",
        "name": "Hebrew University in Jerusalem",
        "college": "",
        "country": "IL",
        "degree": "M.Sc."
    },
    {
        "text": "Master of the ACR",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Master of the ACR"
    },
    {
        "text": "BEng, National University of Singapore",
        "name": "National University of Singapore",
        "college": "",
        "country": "SG",
        "degree": "B.Eng."
    },
    {
        "text": "01/1984 - New York, NY United States",
        "name": "",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "Massachusetts Institute of Technology S.B. Philosophy (1973-1977)",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "S.B. in Philosophy"
    },
    {
        "text": "B.Sc, Rhodes University, Statistics (1975)",
        "name": "Rhodes University",
        "college": "",
        "country": "ZA",
        "degree": "B.Sc. in Statistics"
    },
    {
        "text": "BS in Physics from College of the Holy Cross",
        "name": "College of the Holy Cross",
        "college": "",
        "country": "US",
        "degree": "B.S. in Physics"
    },
    {
        "text": "City College of New York, B.S., 1953-1957",
        "name": "City College of New York",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "PhD in psychology from the University of Michigan in 1977",
        "name": "University of Michigan",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Psychology"
    },
    {
        "text": "Ph.D., Massachusetts Institute of Technology, 1974",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Ph.D. in mathematics from the University of California, Berkeley in 1954",
        "name": "University of California, Berkeley",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Mathematics"
    },
    {
        "text": "University College London (PhD, 1957)",
        "name": "University College London",
        "college": "",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "PhD Harvard University 1976 – 1979",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "B.Sc (hons), Rhodes University, Statistics (1976)",
        "name": "Rhodes University",
        "college": "",
        "country": "ZA",
        "degree": "B.Sc. (Hons) in Statistics"
    },
    {
        "text": "State University College at Buffalo, New York; B.A. degree, December 1971, Magna cum laude",
        "name": "State University College at Buffalo",
        "college": "",
        "country": "US",
        "degree": "B.A. (Magna cum laude)"
    },
    {
        "text": "London School of Economics MSc. June, 1990",
        "name": "London School of Economics",
        "college": "",
        "country": "GB",
        "degree": "M.Sc."
    },
    {
        "text": "medical degree from the University of Toronto",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "Medical Degree"
    },
    {
        "text": "University of Paris VI Maitrise 07/1981 Biochemistry",
        "name": "University of Paris VI",
        "college": "",
        "country": "FR",
        "degree": "Maitrise in Biochemistry"
    },
    {
        "text": "SCD from the Harvard School of Public Health in 1992",
        "name": "Harvard School of Public Health",
        "college": "",
        "country": "US",
        "degree": "SCD"
    },
    {
        "text": "West Virginia Wesleyan College: Buckhannon, WV, US",
        "name": "West Virginia Wesleyan College",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "1961-1965 M.D., Medicine, Yale University, New Haven, CT",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "M.D. in Medicine"
    },
    {
        "text": "Apr 1987-Nov 1988 Polytechnique Montréal Master, Chemical Engineering",
        "name": "Polytechnique Montréal",
        "college": "",
        "country": "CA",
        "degree": "Master in Chemical Engineering"
    },
    {
        "text": "Diploma Swiss Federal Institute of Technology (ETH) Zürich, Department of Chemistry, Switzerland, 1983",
        "name": "Swiss Federal Institute of Technology (ETH) Zürich",
        "college": "Department of Chemistry",
        "country": "CH",
        "degree": "Diploma"
    },
    {
        "text": "A.A. Biology-Biochemistry, College of San Mateo, California - 1967",
        "name": "College of San Mateo",
        "college": "",
        "country": "US",
        "degree": "A.A. in Biology-Biochemistry"
    },
    {
        "text": "undergraduate degree in chemistry from Boston University (1965)",
        "name": "Boston University",
        "college": "",
        "country": "US",
        "degree": "Undergraduate Degree in Chemistry"
    },
    {
        "text": "All India Institute of Medical Science (AIIMS), MD",
        "name": "All India Institute of Medical Science (AIIMS)",
        "college": "",
        "country": "IN",
        "degree": "MD"
    },
    {
        "text": "graduate studies at Johns Hopkins University",
        "name": "Johns Hopkins University",
        "college": "",
        "country": "US",
        "degree": "Graduate Studies"
    },
    {
        "text": "Ph.D.",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D."
    },
    {
        "text": "1974 — baccalauréat — Médecine de famille — Université McGill",
        "name": "Université McGill",
        "college": "",
        "country": "CA",
        "degree": "Baccalauréat in Médecine de famille"
    },
    {
        "text": "post-graduate studies in neuroanatomy at Columbia University",
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "Post-Graduate Studies in Neuroanatomy"
    },
    {
        "text": "Southampton University Hospitals NHS Trust: Southampton, GB 1984 to 1989 | DM",
        "name": "Southampton University Hospitals NHS Trust",
        "college": "",
        "country": "GB",
        "degree": "DM"
    },
    {
        "text": "PhD 1995 University of Glamorgan Mechanical Engineering",
        "name": "University of Glamorgan",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Mechanical Engineering"
    },
    {
        "text": "B.A. (honors), Psychology, San Jose State University, December 1990",
        "name": "San Jose State University",
        "college": "",
        "country": "US",
        "degree": "B.A. (Honors) in Psychology"
    },
    {
        "text": "Diploma degree in Chemistry, 1968 (summa cum laude), Free University of Berlin",
        "name": "Free University of Berlin",
        "college": "",
        "country": "DE",
        "degree": "Diploma in Chemistry"
    },
    {
        "text": "MBBS The University of Adelaide",
        "name": "The University of Adelaide",
        "college": "",
        "country": "AU",
        "degree": "MBBS"
    },
    {
        "text": "R.N. San Joaquin Delta College 1978-1980",
        "name": "San Joaquin Delta College",
        "college": "",
        "country": "US",
        "degree": "R.N."
    }
]
#361-400
d400=[
    {
        "text": "Bachelor of Science Gansu Agricultural University 1984",
        "name": "Gansu Agricultural University",
        "college": "",
        "country": "CN",
        "degree": "Bachelor of Science"
    },
    {
        "text": "Ph.D., Stanford University",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "PhD in Solid State Chemistry, University of Bordeaux, 1981",
        "name": "University of Bordeaux",
        "college": "",
        "country": "FR",
        "degree": "Ph.D. in Solid State Chemistry"
    },
    {
        "text": "University of Edinburgh",
        "name": "University of Edinburgh",
        "college": "",
        "country": "GB",
        "degree": ""
    },
    {
        "text": "University of Pittsburgh MD 05/1982 Medicine",
        "name": "University of Pittsburgh",
        "college": "",
        "country": "US",
        "degree": "MD in Medicine"
    },
    {
        "text": "Ph.D. degree in Information Science at the Helsinki University of Technology in 1997",
        "name": "Helsinki University of Technology",
        "college": "",
        "country": "FI",
        "degree": "Ph.D. in Information Science"
    },
    {
        "text": "1976: Master of Zoological Sciences, with the highest distinction (Free University of Brussels,U.L.B., Belgium).",
        "name": "Free University of Brussels (U.L.B.)",
        "college": "",
        "country": "BE",
        "degree": "Master of Zoological Sciences"
    },
    {
        "text": "1963 Doctorate, TU Munich, Munich, Germany",
        "name": "TU Munich",
        "college": "",
        "country": "DE",
        "degree": "Doctorate"
    },
    {
        "text": "1970-1973 Ivey Business School at Western University Doctor of Philosophy (PhD), Business Administration and Management",
        "name": "Ivey Business School at Western University",
        "college": "",
        "country": "CA",
        "degree": "Ph.D. in Business Administration and Management"
    },
    {
        "text": "MD from Harvard Medical School, 1982",
        "name": "Harvard Medical School",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "1979-1983 Case Western Reserve University School of Medicine Doctor of Medicine (M.D.)",
        "name": "Case Western Reserve University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "M.D. from University of Missouri Medical School 06/1972",
        "name": "University of Missouri Medical School",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "1969-1973, BA, Stanford University",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "S.B.-S.M., Massachusetts Institute of Technology, 1972",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "S.B.-S.M."
    },
    {
        "text": "medical degree (MD) in 1984 at Lund University",
        "name": "Lund University",
        "college": "",
        "country": "SE",
        "degree": "MD"
    },
    {
        "text": "1988 University of Leipzig Biochemistry, Diploma",
        "name": "University of Leipzig",
        "college": "",
        "country": "DE",
        "degree": "Diploma in Biochemistry"
    },
    {
        "text": "MA in Chemistry from Harvard",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "MA in Chemistry"
    },
    {
        "text": "Jan 1994-Aug 1995 Bangalore University: (University Visvesvaraya College of Engineering), India Master of Engineering (ME), Computer Science and Engineering",
        "name": "Bangalore University",
        "college": "University Visvesvaraya College of Engineering",
        "country": "IN",
        "degree": "Master of Engineering (ME) in Computer Science and Engineering"
    },
    {
        "text": "1992, CBiol MIBiol: Biomedical Sciences, Institute of Biology, London",
        "name": "Institute of Biology, London",
        "college": "",
        "country": "GB",
        "degree": "CBiol MIBiol in Biomedical Sciences"
    },
    {
        "text": "M.Phil in Clinical Psychology, Institute of Psychiatry, London, 1985-1987",
        "name": "Institute of Psychiatry, London",
        "college": "",
        "country": "GB",
        "degree": "M.Phil in Clinical Psychology"
    },
    {
        "text": "1964: BSc in chemistry, Leiden University, The Netherlands",
        "name": "Leiden University",
        "college": "",
        "country": "NL",
        "degree": "B.Sc. in Chemistry"
    },
    {
        "text": "MD, University of Otago",
        "name": "University of Otago",
        "college": "",
        "country": "NZ",
        "degree": "MD"
    },
    {
        "text": "Ph.D. in Physics (1978)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D. in Physics"
    },
    {
        "text": "Ch.B. at the University of the Witwatersrand",
        "name": "University of the Witwatersrand",
        "college": "",
        "country": "ZA",
        "degree": "Ch.B."
    },
    {
        "text": "Missouri University of Science and Technology: 1961-08-15 to 1965-06-08 | B.S., Chemistry (Department of Chemistry)",
        "name": "Missouri University of Science and Technology",
        "college": "Department of Chemistry",
        "country": "US",
        "degree": "B.S. in Chemistry"
    },
    {
        "text": "Ph.D. Physical Chemistry, University of California at Berkeley (1960)",
        "name": "University of California at Berkeley",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Physical Chemistry"
    },
    {
        "text": "A.B. degree summa cum laude from Harvard College in 1972-09 to 1976-06",
        "name": "Harvard College",
        "college": "",
        "country": "US",
        "degree": "A.B. summa cum laude"
    },
    {
        "text": "M.D. degree from Johns Hopkins University School of Medicine in 1976-09 to 1980-06",
        "name": "Johns Hopkins University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "September 1977-June 1981 Ph.D Applied Mathematics, University of Illinois At Chicago",
        "name": "University of Illinois At Chicago",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Applied Mathematics"
    },
    {
        "text": "University of California at Berkeley - BA - 1973",
        "name": "University of California at Berkeley",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "1981, Ph.D., University of Kentucky, Chemical Engineering",
        "name": "University of Kentucky",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Chemical Engineering"
    },
    {
        "text": "B.A. Carleton College (1963)",
        "name": "Carleton College",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1978 M.Sc., Organic Chemistry, Technical University of Gdansk, Poland",
        "name": "Technical University of Gdansk",
        "college": "",
        "country": "PL",
        "degree": "M.Sc. in Organic Chemistry"
    },
    {
        "text": "1980-1984 Villanova University Bachelor of Science (B.S.), Biology, General",
        "name": "Villanova University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Biology"
    },
    {
        "text": "Ph.D. University of Regina",
        "name": "University of Regina",
        "college": "",
        "country": "CA",
        "degree": "Ph.D."
    },
    {
        "text": "Ph. D., Inorganic Chemistry, Crystallography, Rutgers University",
        "name": "Rutgers University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Inorganic Chemistry, Crystallography"
    },
    {
        "text": "Humanités anciennes : Athénée Royal d'Etterbeek 1960-1966",
        "name": "Athénée Royal d'Etterbeek",
        "college": "",
        "country": "BE",
        "degree": "Humanités anciennes"
    },
    {
        "text": "Master of Science (MS) Physics 1966 - 1972",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Master of Science (MS) in Physics"
    }
]
#401-433
d433=[
    {
        "text": "1986–1988 M.Sc. in computer science , CGPA 4.0/4.0, Speech recognition with statistical methods, Computer Science Dept., McGill University.",
        "name": "McGill University",
        "college": "Computer Science Dept.",
        "country": "CA",
        "degree": "M.Sc. in Computer Science"
    },
    {
        "text": "M.D. from the University of Pittsburgh School of Medicine in 1984",
        "name": "University of Pittsburgh School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "1948 Hamilton College bachelor's degree in mathematics and physics",
        "name": "Hamilton College",
        "college": "",
        "country": "US",
        "degree": "Bachelor's Degree in Mathematics and Physics"
    },
    {
        "text": "1967 M.D., LMU Munich, Germany",
        "name": "LMU Munich",
        "college": "",
        "country": "DE",
        "degree": "M.D."
    },
    {
        "text": "B.S. in pharmacy, Columbia University, 1962",
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Pharmacy"
    },
    {
        "text": "September 1944-1946 MS degree in electrical engineering from MIT",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "MS in Electrical Engineering"
    },
    {
        "text": "Physical department of the Moscow State University",
        "name": "Moscow State University",
        "college": "Physical Department",
        "country": "RU",
        "degree": ""
    },
    {
        "text": "1985-1989 Massachusetts Institute of Technology BS, Science",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "B.S. in Science"
    },
    {
        "text": "Australian National University 1980-03-01 to 1985-09-05 | PhD (Statistics, Institute of Advanced Studies)",
        "name": "Australian National University",
        "college": "Institute of Advanced Studies",
        "country": "AU",
        "degree": "Ph.D. in Statistics"
    },
    {
        "text": "1960-1963 University of Illinois Urbana-Champaign BS, Pre-Med",
        "name": "University of Illinois Urbana-Champaign",
        "college": "",
        "country": "US",
        "degree": "B.S. in Pre-Med"
    },
    {
        "text": "1975-1978 University of Arizona BS, Range Ecology",
        "name": "University of Arizona",
        "college": "",
        "country": "US",
        "degree": "B.S. in Range Ecology"
    },
    {
        "text": "PhD at Groningen University",
        "name": "Groningen University",
        "college": "",
        "country": "NL",
        "degree": "Ph.D."
    },
    {
        "text": "B.A. in Chemistry, Franklin and Marshall College, 1981",
        "name": "Franklin and Marshall College",
        "college": "",
        "country": "US",
        "degree": "B.A. in Chemistry"
    },
    {
        "text": "May 2004 Brandeis University B.S. in Computer Science",
        "name": "Brandeis University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Computer Science"
    },
    {
        "text": "BA, 1969, Radcliffe College",
        "name": "Radcliffe College",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1962-1964 B.A. Wayne State University",
        "name": "Wayne State University",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "Sept. 1982 - June 1986 Bachelor of Science (B.Sc.) in Chemical Engineering received at Chung-Yuan Christian University in Taiwan",
        "name": "Chung-Yuan Christian University",
        "college": "",
        "country": "TW",
        "degree": "B.Sc. in Chemical Engineering"
    },
    {
        "text": "B.S. 1982, Italian Laurea in Physics (emphasis Atmospheric Sciences), Department of Physics, University of L’Aquila",
        "name": "University of L’Aquila",
        "college": "Department of Physics",
        "country": "IT",
        "degree": "B.S. in Physics"
    },
    {
        "text": "University of Calgary Doctor of Philosophy (Ph.D.), Ecology 1986 - 1989",
        "name": "University of Calgary",
        "college": "",
        "country": "CA",
        "degree": "Ph.D. in Ecology"
    },
    {
        "text": "University of Canterbury Bachelor’s Degree, Botany 1982 - 1985",
        "name": "University of Canterbury",
        "college": "",
        "country": "NZ",
        "degree": "Bachelor’s Degree in Botany"
    },
    {
        "text": "M.D. Columbia University",
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "AB, Physical Sciences, Colgate University",
        "name": "Colgate University",
        "college": "",
        "country": "US",
        "degree": "AB in Physical Sciences"
    },
    {
        "text": "PhD in neuropsychology at Cornell University",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Neuropsychology"
    },
    {
        "text": "1981 B.A. Biology (cum laude), Dartmouth College",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "B.A. in Biology (cum laude)"
    },
    {
        "text": "Ph.D., Duke University, 1973",
        "name": "Duke University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "M.D. from the New York University School of Medicine",
        "name": "New York University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "studied medicine at Nottingham University (1970-1975)",
        "name": "Nottingham University",
        "college": "",
        "country": "GB",
        "degree": ""
    },
    {
        "text": "Ph.D., Delhi University May 1973 - June 1976",
        "name": "Delhi University",
        "college": "",
        "country": "IN",
        "degree": "Ph.D."
    },
    {
        "text": "BS Yale University, Molecular Biophysics & Biochemistry (1984)",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Molecular Biophysics & Biochemistry"
    },
    {
        "text": "1965-09-01 to 1969-09-29 | PhD (Institute of Psychiatry), University Of London",
        "name": "University Of London",
        "college": "Institute of Psychiatry",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "D.Sc.h.c., Niels Bohr Institute, University of Copenhagen.",
        "name": "University of Copenhagen",
        "college": "Niels Bohr Institute",
        "country": "DK",
        "degree": "D.Sc.h.c."
    },
    {
        "text": "1971 Graduate School, Faculty of Medicine, Kyoto University",
        "name": "Kyoto University",
        "college": "Faculty of Medicine",
        "country": "JP",
        "degree": ""
    }
]
#434-460
d460=[
    {
        "text": "1974-1979 Studium der Chemie an der TU Darmstadt, Fachrichtung Physikalische Chemie",
        "name": "TU Darmstadt",
        "college": "",
        "country": "DE",
        "degree": "Studium der Chemie in Physikalische Chemie"
    },
    {
        "text": "B.Sc., 1990, mathematics, McGill University, Canada",
        "name": "McGill University",
        "college": "",
        "country": "CA",
        "degree": "B.Sc. in Mathematics"
    },
    {
        "text": "M.Sc., 1992, mathematics, University of Toronto, Canada",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "M.Sc. in Mathematics"
    },
    {
        "text": "PhD, 1997, mathematics, U of T, Canada",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "Ph.D. in Mathematics"
    },
    {
        "text": "M.Sc., 1997, statistics, U of T, Canada",
        "name": "University of Toronto",
        "college": "",
        "country": "CA",
        "degree": "M.Sc. in Statistics"
    },
    {
        "text": "PhD Department of Chemical Engineering, Ankara University",
        "name": "Ankara University",
        "college": "Department of Chemical Engineering",
        "country": "TR",
        "degree": "Ph.D."
    },
    {
        "text": "Institute of Science & Technology (Karadeniz Technical University) 1977-1980",
        "name": "Karadeniz Technical University",
        "college": "Institute of Science & Technology",
        "country": "TR",
        "degree": ""
    },
    {
        "text": "M Sc. Department of Chemical Engineering, Ankara University, Institute of Science & Technology (Karadeniz Technical University) 1972-1973",
        "name": "Ankara University",
        "college": "Department of Chemical Engineering, Institute of Science & Technology",
        "country": "TR",
        "degree": "M.Sc."
    },
    {
        "text": "B Sc. Department of Chemical Engineering, Ankara University, 1969-1972 Institute of Science & Technology (Karadeniz Technical University) 1969-1972",
        "name": "Ankara University",
        "college": "Department of Chemical Engineering, Institute of Science & Technology",
        "country": "TR",
        "degree": "B.Sc."
    },
    {
        "text": "Corma earned his BS in Chemistry at Valencia University, PhD at Madrid under direction of Prof. Antonio Cortes, and spent two years postdoc at Queen´s University.",
        "name": "Valencia University",
        "college": "",
        "country": "ES",
        "degree": "BS in Chemistry"
    },
    {
        "text": "B.A., University of Pennsylvania, Philadelphia PA 1971",
        "name": "University of Pennsylvania",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1978 - 1984 M.D. (\"Artsexamen\") University of Utrecht",
        "name": "University of Utrecht",
        "college": "",
        "country": "NL",
        "degree": "M.D."
    },
    {
        "text": "Johns Hopkins University, Ph.D in Biophysical Chemistry College of William and Mary, Chemistry and mathematics",
        "name": "Johns Hopkins University",
        "college": "Biophysical Chemistry",
        "country": "US",
        "degree": "Ph.D. in Biophysical Chemistry"
    },
    {
        "text": "PhD 1981-1984, Yale University",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "PhD at Université Joseph-Fourier in Grenoble",
        "name": "Université Joseph-Fourier",
        "college": "",
        "country": "FR",
        "degree": "Ph.D."
    },
    {
        "text": "PhD in 1980 from the ETH Zürich (Biochemistry).",
        "name": "ETH Zürich",
        "college": "",
        "country": "CH",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "1953, PhD, Johns Hopkins University",
        "name": "Johns Hopkins University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Ph.D. in electrical engineering, Georgia Institute of Technology, 1981",
        "name": "Georgia Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Electrical Engineering"
    },
    {
        "text": "BS, Tongji University, Shanghai, China 1982",
        "name": "Tongji University",
        "college": "",
        "country": "CN",
        "degree": "B.S."
    },
    {
        "text": "B.Sc (1972) Université McGill",
        "name": "Université McGill",
        "college": "",
        "country": "CA",
        "degree": "B.Sc."
    },
    {
        "text": "Albany Medical College, Union University",
        "name": "Albany Medical College",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "BA 1953 Columbia",
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "BA"
    },
    {
        "text": "1982, University of North Dakota BA Mathematics",
        "name": "University of North Dakota",
        "college": "",
        "country": "US",
        "degree": "BA in Mathematics"
    },
    {
        "text": "B.A. 1965 (Math) Colorado College (summa cum laude)",
        "name": "Colorado College",
        "college": "",
        "country": "US",
        "degree": "B.A. in Math (summa cum laude)"
    },
    {
        "text": "1970 PhD at Stanford University",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "January 1988: PhD (Plant Nutritional Physiology), Hohenheim University, Stuttgart.",
        "name": "Hohenheim University",
        "college": "",
        "country": "DE",
        "degree": "Ph.D. in Plant Nutritional Physiology"
    },
    {
        "text": "1983-1987-05-01 University of Ljubljana, Slovenia BSc Chemistry",
        "name": "University of Ljubljana",
        "college": "",
        "country": "SI",
        "degree": "B.Sc. in Chemistry"
    },
    {
        "text": "1965 B.A. Dartmouth College, Hanover, New Hampshire",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "College, University of Missouri-St. Louis St. Louis, MO (1975)",
        "name": "University of Missouri-St. Louis",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "Doctorat-ès-Sciences (Ph.D.), University of Strasbourg, 1963",
        "name": "University of Strasbourg",
        "college": "",
        "country": "FR",
        "degree": "Doctorat-ès-Sciences (Ph.D.)"
    },
    {
        "text": "1976 University of California, Los Angeles PhD Biochemistry",
        "name": "University of California, Los Angeles",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "1972 American University of Beirut, Beirut, LBN, BaccalaureateII",
        "name": "American University of Beirut",
        "college": "",
        "country": "LB",
        "degree": "BaccalaureateII"
    },
    {
        "text": "Ph.D. thesis was completed at Harvard Medical School in the lab of Michael Greenberg.",
        "name": "Harvard Medical School",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    }
]
#461-490
d490=[
    {
        "text": "B.S., Massachusetts Institute of Technology, 1964/6",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "Universität Hannover Diplom 1992 – 1997",
        "name": "Universität Hannover",
        "college": "",
        "country": "DE",
        "degree": "Diplom"
    },
    {
        "text": "2002 to 2007 University of Maribor, physics, PhD",
        "name": "University of Maribor",
        "college": "",
        "country": "SI",
        "degree": "Ph.D. in Physics"
    },
    {
        "text": "1987 - 29.06.1989 PhD, University of Göttingen",
        "name": "University of Göttingen",
        "college": "",
        "country": "DE",
        "degree": "Ph.D."
    },
    {
        "text": "Stanford University M.D. - 1970",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "BA University of York",
        "name": "University of York",
        "college": "",
        "country": "GB",
        "degree": "BA"
    },
    {
        "text": "DPhil University of Oxford",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "DPhil"
    },
    {
        "text": "Ph.D., Columbia University, New York, 1988, Pharmacology",
        "name": "Columbia University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Pharmacology"
    },
    {
        "text": "Pharm.D., University of Naples, Italy, 1982",
        "name": "University of Naples",
        "college": "",
        "country": "IT",
        "degree": "Pharm.D."
    },
    {
        "text": "Ph.D. Physics, University of Cambridge, U.K. 1972",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Physics"
    },
    {
        "text": "M.S. Mechanical Engineering, University of Minnesota 1969",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "M.S. in Mechanical Engineering"
    },
    {
        "text": "B.M.E. Mechanical Engineering, University of Minnesota 1967",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "B.M.E. in Mechanical Engineering"
    },
    {
        "text": "University of London PhD, Cell/Cellular and Molecular Biology",
        "name": "University of London",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Cell/Cellular and Molecular Biology"
    },
    {
        "text": "MD: University of Illinois, Chicago (1977)",
        "name": "University of Illinois, Chicago",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "M.E. degree in Mechanical Engineering from Pratt Institute",
        "name": "Pratt Institute",
        "college": "",
        "country": "US",
        "degree": "M.E. in Mechanical Engineering"
    },
    {
        "text": "1981-1985 Harvard Medical School MD, Medicine",
        "name": "Harvard Medical School",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "M.Sc., degree from the Silesian University of Technology, Gliwice, Poland, in 1977",
        "name": "Silesian University of Technology",
        "college": "",
        "country": "PL",
        "degree": "M.Sc."
    },
    {
        "text": "1972 - 1975 Graduate Student, Lebedev Physical Institute, Moscow",
        "name": "Lebedev Physical Institute",
        "college": "",
        "country": "RU",
        "degree": "Graduate Student"
    },
    {
        "text": "1980-1987 University of Minnesota (most part) Master of Science of Public Health, MScPH",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "Master of Science of Public Health (MScPH)"
    },
    {
        "text": "MD from the University of Pennsylvania School of Medicine in 1975",
        "name": "University of Pennsylvania School of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "bachelor's degree in neurobiology from Vassar College in 1959",
        "name": "Vassar College",
        "college": "",
        "country": "US",
        "degree": "Bachelor's Degree in Neurobiology"
    },
    {
        "text": "In 1970, Doctor of Philosophy at the University of Oxford",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "MS: 1968, Comparative Psychology, University of Georgia",
        "name": "University of Georgia",
        "college": "",
        "country": "US",
        "degree": "M.S. in Comparative Psychology"
    },
    {
        "text": "Bachelor of Arts degree in Biochemistry and Chemistry from Brandeis University in 1983",
        "name": "Brandeis University",
        "college": "",
        "country": "US",
        "degree": "Bachelor of Arts in Biochemistry and Chemistry"
    },
    {
        "text": "1977-1980, Cornell University, Doctorate in regional science",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "Doctorate in Regional Science"
    },
    {
        "text": "BSc, University of Alberta, 1983",
        "name": "University of Alberta",
        "college": "",
        "country": "CA",
        "degree": "B.Sc."
    },
    {
        "text": "B.S. in Electrical Engineering, Indian Institute of Technology, Kanpur, 1980",
        "name": "Indian Institute of Technology, Kanpur",
        "college": "",
        "country": "IN",
        "degree": "B.S. in Electrical Engineering"
    },
    {
        "text": "PhD – Australian National University, Canberra in 1962",
        "name": "Australian National University",
        "college": "",
        "country": "AU",
        "degree": "Ph.D."
    },
    {
        "text": "doctorate at the University of Helsinki",
        "name": "University of Helsinki",
        "college": "",
        "country": "FI",
        "degree": "Doctorate"
    },
    {
        "text": "June 1983, Diploma of Chemistry",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Diploma of Chemistry"
    },
    {
        "text": "B.S., 1973",
        "name": "",
        "college": "",
        "country": "",
        "degree": "B.S."
    },
    {
        "text": "B.S. degree from Iowa State University",
        "name": "Iowa State University",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "D.Phil. (1979) degree at the University of Oxford",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "D.Phil."
    },
    {
        "text": "Bachelor of Science, Monash University",
        "name": "Monash University",
        "college": "",
        "country": "AU",
        "degree": "Bachelor of Science"
    }
]
#491-520
d520=[
    {
        "text": "University of Cambridge (BA)",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "BA"
    },
    {
        "text": "PhD: Physics and Applied Physics, U-Mass., Lowell, 1992",
        "name": "University of Massachusetts, Lowell",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Physics and Applied Physics"
    },
    {
        "text": "M.S., Kyoto University, Kyoto Japan, 1955",
        "name": "Kyoto University",
        "college": "",
        "country": "JP",
        "degree": "M.S."
    },
    {
        "text": "1989 BSc in Biochem. Mol.Biol at Autónoma University, Madrid, Spain",
        "name": "Autónoma University, Madrid",
        "college": "",
        "country": "ES",
        "degree": "B.Sc. in Biochemistry and Molecular Biology"
    },
    {
        "text": "University of Buenos Aires (M.D., 1969)",
        "name": "University of Buenos Aires",
        "college": "",
        "country": "AR",
        "degree": "M.D."
    },
    {
        "text": "MS University of California, Los Angeles, Biochemistry and Molecular Biology (1999)",
        "name": "University of California, Los Angeles",
        "college": "",
        "country": "US",
        "degree": "M.S. in Biochemistry and Molecular Biology"
    },
    {
        "text": "undergraduate degree in psychology from Princeton University",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "Undergraduate degree in Psychology"
    },
    {
        "text": "Rockefeller University Ph.D. 1988",
        "name": "Rockefeller University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Jul 1988-Aug 1992 University of Mysore (J. M. Institute of Technology), India Bachelor of Engineering (B.E), Computer Science and Engineering",
        "name": "University of Mysore (J. M. Institute of Technology)",
        "college": "",
        "country": "IN",
        "degree": "Bachelor of Engineering (B.E) in Computer Science and Engineering"
    },
    {
        "text": "1974-1979 York University BSc, Psychobiology & Neurochemistry",
        "name": "York University",
        "college": "",
        "country": "CA",
        "degree": "B.Sc. in Psychobiology & Neurochemistry"
    },
    {
        "text": "University of Auckland, New Zealand, Ph.D., 1974, Psychology",
        "name": "University of Auckland",
        "college": "",
        "country": "NZ",
        "degree": "Ph.D. in Psychology"
    },
    {
        "text": "doctorate from the University of Vienna (1992)",
        "name": "University of Vienna",
        "college": "",
        "country": "AT",
        "degree": "Doctorate"
    },
    {
        "text": "1993 M.Sc. University Of Tartu.",
        "name": "University Of Tartu",
        "college": "",
        "country": "EE",
        "degree": "M.Sc."
    },
    {
        "text": "North Carolina at Chapel Hill, USA, in 1988",
        "name": "North Carolina at Chapel Hill",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "Medical School: Columbia University College of Physicians and Surgeons",
        "name": "Columbia University College of Physicians and Surgeons",
        "college": "",
        "country": "US",
        "degree": "Medical School"
    },
    {
        "text": "1990 PhD - The Australian National University",
        "name": "The Australian National University",
        "college": "",
        "country": "AU",
        "degree": "Ph.D."
    },
    {
        "text": "1985 Medical School at the University of Newcastle upon Tyne",
        "name": "University of Newcastle upon Tyne",
        "college": "Medical School",
        "country": "GB",
        "degree": "Medical Degree"
    },
    {
        "text": "1980: B.S. Faculty of Engineering, Chiba University",
        "name": "Chiba University",
        "college": "Faculty of Engineering",
        "country": "JP",
        "degree": "B.S."
    },
    {
        "text": "MD (Medicine) University of California in San Francisco",
        "name": "University of California in San Francisco",
        "college": "",
        "country": "US",
        "degree": "MD in Medicine"
    },
    {
        "text": "SB, 1983, Biology, Harvard University",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "SB in Biology"
    },
    {
        "text": "Massachusetts Institute of Technology S.B., mathematics, 1982–1985.",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "S.B. in Mathematics"
    },
    {
        "text": "graduated from the National School of Chemistry of Strasbourg (now known as ECPM Strasbourg), in 1967",
        "name": "National School of Chemistry of Strasbourg",
        "college": "",
        "country": "FR",
        "degree": ""
    },
    {
        "text": "PhD degree from the Université Louis-Pasteur",
        "name": "Université Louis-Pasteur",
        "college": "",
        "country": "FR",
        "degree": "Ph.D."
    },
    {
        "text": "UNDERGRADUATE STUDIES, University of Neuchâtel, Switzerland, Licence es Sciences Économiques, 1975.",
        "name": "University of Neuchâtel",
        "college": "",
        "country": "CH",
        "degree": "Licence es Sciences Économiques"
    },
    {
        "text": "2003 DSc - The Australian National University",
        "name": "The Australian National University",
        "college": "",
        "country": "AU",
        "degree": "DSc"
    },
    {
        "text": "MD University of Heidelberg Medical School 1985",
        "name": "University of Heidelberg Medical School",
        "college": "",
        "country": "DE",
        "degree": "MD"
    },
    {
        "text": "undergarduate degree from Presidency College in Calcutta (Kolkata), India",
        "name": "Presidency College, Kolkata",
        "college": "",
        "country": "IN",
        "degree": "Undergraduate degree"
    },
    {
        "text": "Fellow - Special Clinical Fellow Department of Neurology, Mayo School of Graduate Medical Education, Mayo Clinic College of Medicine, Department of Education Administration",
        "name": "Mayo Clinic College of Medicine",
        "college": "Department of Neurology",
        "country": "US",
        "degree": "Fellow - Special Clinical Fellow"
    },
    {
        "text": "Research Fellowship - Visiting Neurologist and Research Fellow Neurological-Neurosurgical ICU, Massachusetts General Hospital, Harvard University",
        "name": "Massachusetts General Hospital",
        "college": "Neurological-Neurosurgical ICU",
        "country": "US",
        "degree": "Research Fellowship"
    },
    {
        "text": "Fellow - Clinical Neurophysiology Department of Neurophysiology, Dijkzigt Hospital, Erasmus University",
        "name": "Dijkzigt Hospital, Erasmus University",
        "college": "Department of Neurophysiology",
        "country": "NL",
        "degree": "Fellow - Clinical Neurophysiology"
    },
    {
        "text": "Resident - Neurology Department of Neurology, Dijkzigt Hospital, Erasmus University",
        "name": "Dijkzigt Hospital, Erasmus University",
        "college": "Department of Neurology",
        "country": "NL",
        "degree": "Resident - Neurology"
    },
    {
        "text": "Resident - Psychiatry Department of Psychiatry, Wassenaar, University of Leiden",
        "name": "University of Leiden",
        "college": "Department of Psychiatry",
        "country": "NL",
        "degree": "Resident - Psychiatry"
    },
    {
        "text": "Resident - Internal Medicine Department of Internal Medicine, Bleuland Hospital, Gouda, University of Leiden",
        "name": "University of Leiden",
        "college": "Department of Internal Medicine",
        "country": "NL",
        "degree": "Resident - Internal Medicine"
    },
    {
        "text": "MD Medical School, University of Leiden",
        "name": "University of Leiden",
        "college": "Medical School",
        "country": "NL",
        "degree": "MD"
    },
    {
        "text": "BS.: Physics, National Cheng-Kung University, Taiwan, 1982",
        "name": "National Cheng-Kung University",
        "college": "",
        "country": "TW",
        "degree": "B.S. in Physics"
    },
    {
        "text": "1988 Interdisciplinary Graduate school of Science and Engineering, Tokyo Institute of Technology (Doctor)",
        "name": "Tokyo Institute of Technology",
        "college": "Interdisciplinary Graduate School of Science and Engineering",
        "country": "JP",
        "degree": "Doctor"
    },
    {
        "text": "PhD from University of Paris",
        "name": "University of Paris",
        "college": "",
        "country": "FR",
        "degree": "Ph.D."
    }
]
#521-560
d560=[
    {
        "text": "Ph.D. from the University of Illinois at Urbana-Champaign in 1979",
        "name": "University of Illinois at Urbana-Champaign",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "B.A. Princeton University 1987",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "1968-1972 Icahn School of Medicine at Mount Sinai Doctor of Medicine (M.D.)",
        "name": "Icahn School of Medicine at Mount Sinai",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "MD from Kobe University in 1987",
        "name": "Kobe University",
        "college": "",
        "country": "JP",
        "degree": "MD"
    },
    {
        "text": "B.Sc University of Cape Town 1969",
        "name": "University of Cape Town",
        "college": "",
        "country": "ZA",
        "degree": "B.Sc."
    },
    {
        "text": "1971-1974 Western Washington University BS, Biology",
        "name": "Western Washington University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Biology"
    },
    {
        "text": "1992, PhD: Doctor of Philosophy in Orthopaedics, University of London",
        "name": "University of London",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Orthopaedics"
    },
    {
        "text": "Doctor of Medicine, Alpha Omega Alpha 1985-1989 University of Rochester School of Medicine & Dentistry",
        "name": "University of Rochester School of Medicine & Dentistry",
        "college": "",
        "country": "US",
        "degree": "Doctor of Medicine"
    },
    {
        "text": "1960 Massachusetts Institute of Technology, B.S. in Physics",
        "name": "Massachusetts Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "B.S. in Physics"
    },
    {
        "text": "MD The Ohio State University, College of Medicine",
        "name": "The Ohio State University, College of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "The University of Texas at Austin, BA, Zoology/ Cell Biology, 1966",
        "name": "The University of Texas at Austin",
        "college": "",
        "country": "US",
        "degree": "BA in Zoology/Cell Biology"
    },
    {
        "text": "The University of Kansas at Lawrence, MA, Cell Biol. & Physiol.Mol. Cell., 1968",
        "name": "The University of Kansas at Lawrence",
        "college": "",
        "country": "US",
        "degree": "MA in Cell Biology & Physiology"
    },
    {
        "text": "The University of Colorado at Boulder, PhD, Develop. Biology, 1972-1975",
        "name": "The University of Colorado at Boulder",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Developmental Biology"
    },
    {
        "text": "B.A. (1st class honors) from Oxford University and obtained his medical degree and training at London University",
        "name": "Oxford University",
        "college": "",
        "country": "GB",
        "degree": "B.A. (1st class honors)"
    },
    {
        "text": "B.A., Chemistry, Temple University",
        "name": "Temple University",
        "college": "",
        "country": "US",
        "degree": "B.A. in Chemistry"
    },
    {
        "text": "MD, Johns Hopkins University School of Medicine (1976)",
        "name": "Johns Hopkins University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "1978, M.S., University of Kentucky, Chemical Engineering",
        "name": "University of Kentucky",
        "college": "",
        "country": "US",
        "degree": "M.S. in Chemical Engineering"
    },
    {
        "text": "1 Oct 1969 - 30 Jun 1972 BA Sociology University of Essex",
        "name": "University of Essex",
        "college": "",
        "country": "GB",
        "degree": "BA in Sociology"
    },
    {
        "text": "Medical Degree: University of Cincinnati Cincinnati, OH, 1982 (Neurology)",
        "name": "University of Cincinnati",
        "college": "",
        "country": "US",
        "degree": "MD in Neurology"
    },
    {
        "text": "Study of chemistry Free Univ. of Berlin",
        "name": "Free University of Berlin",
        "college": "",
        "country": "DE",
        "degree": "Study of Chemistry"
    },
    {
        "text": "Postgraduate Diploma, 1966, Theoretical Physics, Charles University, Prague, Czech Republic",
        "name": "Charles University",
        "college": "",
        "country": "CZ",
        "degree": "Postgraduate Diploma in Theoretical Physics"
    },
    {
        "text": "1975 Ph.D. Faculty of Engineering, Kyoto University",
        "name": "Kyoto University",
        "college": "Faculty of Engineering",
        "country": "JP",
        "degree": "Ph.D."
    },
    {
        "text": "1988 Master of Medical Sciences KU Leuven",
        "name": "KU Leuven",
        "college": "",
        "country": "BE",
        "degree": "Master of Medical Sciences"
    },
    {
        "text": "1964-1965 Clark University",
        "name": "Clark University",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "MD in 1973 at Gothenburg University",
        "name": "Gothenburg University",
        "college": "",
        "country": "SE",
        "degree": "MD"
    },
    {
        "text": "1971-1973 BA (with honors) University of Florida, Gainesville, FL, Architecture",
        "name": "University of Florida",
        "college": "",
        "country": "US",
        "degree": "BA in Architecture"
    },
    {
        "text": "BAppScience (1987). Royal Melbourne Institute of Technology (Australia).",
        "name": "Royal Melbourne Institute of Technology",
        "college": "",
        "country": "AU",
        "degree": "BAppScience"
    },
    {
        "text": "University College London (MSc) 1975",
        "name": "University College London",
        "college": "",
        "country": "GB",
        "degree": "MSc"
    },
    {
        "text": "Medical School Johns Hopkins University School of Medicine",
        "name": "Johns Hopkins University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "Medical School"
    },
    {
        "text": "1982–1986: B.Sc. in Electrical Engineering–The Technion",
        "name": "The Technion",
        "college": "",
        "country": "IL",
        "degree": "B.Sc. in Electrical Engineering"
    },
    {
        "text": "Ph.D. from Harvard University in 1983",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Master of Public Health, University of Washington",
        "name": "University of Washington",
        "college": "",
        "country": "US",
        "degree": "Master of Public Health"
    },
    {
        "text": "MD, Yale University School of Medicine",
        "name": "Yale University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "Thèse de Doctorat d'Etat ès Sciences Physiques (Université de Paris VI, 10 janvier 1979)",
        "name": "Université de Paris VI",
        "college": "",
        "country": "FR",
        "degree": "Doctorat d'Etat ès Sciences Physiques"
    },
    {
        "text": "Universität Basel Doctor of Philosophy (PhD) 1999 – 2001",
        "name": "Universität Basel",
        "college": "",
        "country": "CH",
        "degree": "Ph.D."
    },
    {
        "text": "1976 Diplôme d'Étude Approfondie, Decision Mathematics, Paris IX -Dauphine",
        "name": "Paris IX -Dauphine",
        "college": "",
        "country": "FR",
        "degree": "Diplôme d'Étude Approfondie"
    },
    {
        "text": "1968-1976 University of Wisconsin, Madison WI Master of Science (M.S.), Biochemistry",
        "name": "University of Wisconsin, Madison WI",
        "college": "",
        "country": "US",
        "degree": "M.S. in Biochemistry"
    },
    {
        "text": "Bachelor’s degree in Physics from the University of Science and Technology of China in 2004",
        "name": "University of Science and Technology of China",
        "college": "",
        "country": "CN",
        "degree": "Bachelor’s degree in Physics"
    },
    {
        "text": "PH. D. 1977",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D."
    },
    {
        "text": "PhD: 1971, Neuropsychology, Purdue University",
        "name": "Purdue University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Neuropsychology"
    },
    {
        "text": "BS degrees in Chemical Engineering at Tokyo Institute of Technology in 1973",
        "name": "Tokyo Institute of Technology",
        "college": "",
        "country": "JP",
        "degree": "B.S. in Chemical Engineering"
    },
    {
        "text": "MD degree in 1965",
        "name": "",
        "college": "",
        "country": "",
        "degree": "MD"
    }
]
#561-590
d590=[
    {
        "text": "Ph.D., Physiology, UCLA, Los Angeles CA 1978",
        "name": "UCLA",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Physiology"
    },
    {
        "text": "B.A., Biology, University of Colorado, Boulder CO 1974",
        "name": "University of Colorado",
        "college": "",
        "country": "US",
        "degree": "B.A. in Biology"
    },
    {
        "text": "University of California, Los Angeles, Ph.D., 1978, Social Psychology",
        "name": "University of California, Los Angeles",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Social Psychology"
    },
    {
        "text": "2000-02-01 | PhD (Chemistry) (Department of Chemistry) Technical University of Denmark",
        "name": "Technical University of Denmark",
        "college": "Department of Chemistry",
        "country": "DK",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "Princeton University, Doctor of Philosophy - PhD, Computer Science, Sep 1992 - Jun 1996",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Computer Science"
    },
    {
        "text": "1974-1975: M.Sc. Medical Physics, Surrey University",
        "name": "Surrey University",
        "college": "",
        "country": "GB",
        "degree": "M.Sc. in Medical Physics"
    },
    {
        "text": "Feb. 1972 Ph.D. (\"Geaggregeerde voor het Hoger Onderwijs in de Geneeskunde\"), K.U. Leuven, Belgium",
        "name": "K.U. Leuven",
        "college": "",
        "country": "BE",
        "degree": "Ph.D. in Medicine"
    },
    {
        "text": "1957, BS Physics and Mathematics, University of Nebraska-Lincoln",
        "name": "University of Nebraska-Lincoln",
        "college": "",
        "country": "US",
        "degree": "B.S. in Physics and Mathematics"
    },
    {
        "text": "Ph.D., M. Curie-Sklodowska University (Poland), 1976",
        "name": "M. Curie-Sklodowska University",
        "college": "",
        "country": "PL",
        "degree": "Ph.D."
    },
    {
        "text": "PhD Chemical Engineering University of Minnesota",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Chemical Engineering"
    },
    {
        "text": "MS Chemical Engineering University of Minnesota",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "M.S. in Chemical Engineering"
    },
    {
        "text": "BS Chemical Engineering University of Minnesota",
        "name": "University of Minnesota",
        "college": "",
        "country": "US",
        "degree": "B.S. in Chemical Engineering"
    },
    {
        "text": "1979-1984 Stanford University School of Medicine Biochemistry",
        "name": "Stanford University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "Biochemistry"
    },
    {
        "text": "1986 Diplom Ingenieur in Engineering Physics (eq. MS)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Diplom Ingenieur in Engineering Physics"
    },
    {
        "text": "1986 (B.S.) Dept. of Chemical Engineering, Seoul National University, Seoul, Korea",
        "name": "Seoul National University",
        "college": "Dept. of Chemical Engineering",
        "country": "KR",
        "degree": "B.S. in Chemical Engineering"
    },
    {
        "text": "University of Reading 1980 , PhD (Applied Statistics)",
        "name": "University of Reading",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Applied Statistics"
    },
    {
        "text": "B.A. 05/1977 - University of North Carolina, Chapel Hill",
        "name": "University of North Carolina, Chapel Hill",
        "college": "",
        "country": "US",
        "degree": "B.A."
    },
    {
        "text": "DSc from Queen's College, Oxford University in 2000",
        "name": "Oxford University",
        "college": "Queen's College",
        "country": "GB",
        "degree": "DSc"
    },
    {
        "text": "MD, 1983 Parma University (Parma, Italy)",
        "name": "Parma University",
        "college": "",
        "country": "IT",
        "degree": "MD"
    },
    {
        "text": "MD, University of Athens School of Medicine, Athens, Greece, Medicine (1990)",
        "name": "University of Athens School of Medicine",
        "college": "",
        "country": "GR",
        "degree": "MD in Medicine"
    },
    {
        "text": "Stanford University, Ph.D., 1972",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1955-1959 B.Sc., Magna Cum Laude, McGill University",
        "name": "McGill University",
        "college": "",
        "country": "CA",
        "degree": "B.Sc. (Magna Cum Laude)"
    },
    {
        "text": "Bachelor of Science with Honors (Magna Cum Laude), Winona State University, Winona, Minnesota, August 1991",
        "name": "Winona State University",
        "college": "",
        "country": "US",
        "degree": "Bachelor of Science with Honors"
    },
    {
        "text": "Polytechnic Institute of Brooklyn",
        "name": "Polytechnic Institute of Brooklyn",
        "college": "",
        "country": "US",
        "degree": ""
    },
    {
        "text": "B. Commerce (with Honors) Management Al-Azhar University",
        "name": "Al-Azhar University",
        "college": "",
        "country": "EG",
        "degree": "B. Commerce in Management"
    },
    {
        "text": "The University of Utah Medical Education, MD, 1986",
        "name": "The University of Utah",
        "college": "Medical Education",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "University of Valencia, Spain M.D. 1984-09-01 to 1990-06-30",
        "name": "University of Valencia",
        "college": "",
        "country": "ES",
        "degree": "M.D."
    },
    {
        "text": "1967-1972 studied Biochemistry at the University of Tübingen",
        "name": "University of Tübingen",
        "college": "",
        "country": "DE",
        "degree": "Biochemistry"
    },
    {
        "text": "Jul 1986-Oct 1990 Indian Institute of Technology, Roorkee Doctor of Philosophy - PhD, Chemistry",
        "name": "Indian Institute of Technology, Roorkee",
        "college": "",
        "country": "IN",
        "degree": "Ph.D. in Chemistry"
    },
    {
        "text": "1997 Ph.D. Biology, University of Colorado, Boulder",
        "name": "University of Colorado, Boulder",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biology"
    },
    {
        "text": "1995 M.S. Geography (ecology), University of Colorado, Boulder",
        "name": "University of Colorado, Boulder",
        "college": "",
        "country": "US",
        "degree": "M.S. in Geography (Ecology)"
    },
    {
        "text": "1991 B.S. Engineering (radiative physics), University of Colorado, Boulder",
        "name": "University of Colorado, Boulder",
        "college": "",
        "country": "US",
        "degree": "B.S. in Engineering (Radiative Physics)"
    },
    {
        "text": "B.S., Rockhurst College, cum laude, 1969",
        "name": "Rockhurst College",
        "college": "",
        "country": "US",
        "degree": "B.S. (cum laude)"
    },
    {
        "text": "Stanford University, M.S., 1961-1964",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "M.S."
    },
    {
        "text": "London School of Economics PhD",
        "name": "London School of Economics",
        "college": "",
        "country": "GB",
        "degree": "Ph.D."
    }
]
#591-620
d620=[
    {
        "text": "MD Cornell University Medical College (1991)",
        "name": "Cornell University Medical College",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "1958 B.S. in Biology at the Long Island University",
        "name": "Long Island University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Biology"
    },
    {
        "text": "Ph.D of Pharmaceutical Biotechnology Mashhad University of Medical Sciences, Mashahd, Iran",
        "name": "Mashhad University of Medical Sciences",
        "college": "",
        "country": "IR",
        "degree": "Ph.D. in Pharmaceutical Biotechnology"
    },
    {
        "text": "1977-1980 University of Eastern Finland PhD, Epidemiology",
        "name": "University of Eastern Finland",
        "college": "",
        "country": "FI",
        "degree": "Ph.D. in Epidemiology"
    },
    {
        "text": "Florida State University, Tallahassee, Florida; M.S. degree, August 1974",
        "name": "Florida State University",
        "college": "",
        "country": "US",
        "degree": "M.S."
    },
    {
        "text": "University of Vienna, Vienna, Austria, 1969.",
        "name": "University of Vienna",
        "college": "",
        "country": "AT",
        "degree": ""
    },
    {
        "text": "B.A. (German) King's College (1965-1967 & 1969-1970), 1970.",
        "name": "King's College",
        "college": "",
        "country": "GB",
        "degree": "B.A. in German"
    },
    {
        "text": "Erasmus University Rotterdam, Rotterdam, The Netherlands, 1974.",
        "name": "Erasmus University Rotterdam",
        "college": "",
        "country": "NL",
        "degree": ""
    },
    {
        "text": "M.D. Tufts University School of Medicine, 1976.",
        "name": "Tufts University School of Medicine",
        "college": "",
        "country": "US",
        "degree": "M.D."
    },
    {
        "text": "Ph.D. (Neuroanatomy) Tufts University Graduate School of Arts and Sciences, 1976.",
        "name": "Tufts University Graduate School of Arts and Sciences",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Neuroanatomy"
    },
    {
        "text": "PhD: Medical College of Wisconsin, 1994",
        "name": "Medical College of Wisconsin",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "1978 to 1981 , B. Sc. Bichemistry, Université de Genève Faculté des Sciences",
        "name": "Université de Genève",
        "college": "Faculté des Sciences",
        "country": "CH",
        "degree": "B.Sc. in Biochemistry"
    },
    {
        "text": "1984-1985 Engineering Diploma, ¡Ecole Nationale Sup´erieure des T´el´ecommunications of Paris",
        "name": "Ecole Nationale Sup´erieure des T´el´ecommunications of Paris",
        "college": "",
        "country": "FR",
        "degree": "Engineering Diploma"
    },
    {
        "text": "1959, graduate of Dartmouth College",
        "name": "Dartmouth College",
        "college": "",
        "country": "US",
        "degree": "Graduate"
    },
    {
        "text": "1987-1988 Ruhr University Bochum physikum, Pre-Medicine/Pre-Medical Studies",
        "name": "Ruhr University Bochum",
        "college": "",
        "country": "DE",
        "degree": "Physikum"
    },
    {
        "text": "Ph.D. in 1949",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D."
    },
    {
        "text": "1992 University of Kansas Medical Center, Kansas City, KS, USA, PHD, Biochemistry and Molecular Biology",
        "name": "University of Kansas Medical Center",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biochemistry and Molecular Biology"
    },
    {
        "text": "1994-1998 Ph.D. Stanford University (Neuroscience)",
        "name": "Stanford University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Neuroscience"
    },
    {
        "text": "1970 MD, University of Hamburg, Medical School, Germany",
        "name": "University of Hamburg Medical School",
        "college": "",
        "country": "DE",
        "degree": "MD"
    },
    {
        "text": "A.B., Harvard University, 1978",
        "name": "Harvard University",
        "college": "",
        "country": "US",
        "degree": "A.B."
    },
    {
        "text": "1981-10-01 to 1985-06-30 , BA (Mod) (Biochemistry) SUNY - Upstate Medical Center",
        "name": "SUNY - Upstate Medical Center",
        "college": "",
        "country": "US",
        "degree": "BA in Biochemistry"
    },
    {
        "text": "A. S., Biology, Santa Rosa Junior College, 1980",
        "name": "Santa Rosa Junior College",
        "college": "",
        "country": "US",
        "degree": "A.S. in Biology"
    },
    {
        "text": "B. S., Bacteriology, University of California Davis, 1982",
        "name": "University of California Davis",
        "college": "",
        "country": "US",
        "degree": "B.S. in Bacteriology"
    },
    {
        "text": "Ph. D., Marine Biology, Scripps Institute of Oceanography, 1986",
        "name": "Scripps Institute of Oceanography",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Marine Biology"
    },
    {
        "text": "1982 Ph.D. University of Aberdeen, Department of Botany",
        "name": "University of Aberdeen",
        "college": "Department of Botany",
        "country": "GB",
        "degree": "Ph.D."
    },
    {
        "text": "King's College, Cambridge, BA 1963",
        "name": "King's College, Cambridge",
        "college": "",
        "country": "GB",
        "degree": "BA"
    },
    {
        "text": "received Ph.D. in Oceanography at the Scripps Institution of Oceanography, University of California, San Diego, in 1977.",
        "name": "Scripps Institution of Oceanography, University of California, San Diego",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Oceanography"
    },
    {
        "text": "1986 to 1988 | Pre-diploma (with distinction) (Physics) Universität Hamburg",
        "name": "Universität Hamburg",
        "college": "",
        "country": "DE",
        "degree": "Pre-diploma in Physics"
    },
    {
        "text": "Ph.D. Cornell University, Ithaca, NY, 1976.",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "Yale University: 1982-09-01 to 1988-05-20 | PhD (Geology and Geophysics)",
        "name": "Yale University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Geology and Geophysics"
    },
    {
        "text": "1995, Pure an Applied Chemistry, University of Strathclyde, DSc",
        "name": "University of Strathclyde",
        "college": "",
        "country": "GB",
        "degree": "DSc in Pure and Applied Chemistry"
    },
    {
        "text": "1969 - 1972, Pure and Applied Chemistry, University of Strathclyde, PhD",
        "name": "University of Strathclyde",
        "college": "",
        "country": "GB",
        "degree": "Ph.D. in Pure and Applied Chemistry"
    },
    {
        "text": "1966 - 1969, Pure and Applied Chemistry, University of Strathclyde, BSc",
        "name": "University of Strathclyde",
        "college": "",
        "country": "GB",
        "degree": "BSc in Pure and Applied Chemistry"
    },
    {
        "text": "1957–1962, University of Bern, Switzerland: Lizentiat in chemistry, physics and mathematics.",
        "name": "University of Bern",
        "college": "",
        "country": "CH",
        "degree": "Lizentiat in Chemistry, Physics, and Mathematics"
    },
    {
        "text": "MD, University of Cincinnati College of Medicine",
        "name": "University of Cincinnati College of Medicine",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "Ph.D., Queen’s University, Canada, 1972 to 1975",
        "name": "Queen’s University",
        "college": "",
        "country": "CA",
        "degree": "Ph.D."
    },
    {
        "text": "studied 2 years of electromechanical engineering at Universidad Tecnologica Nacional",
        "name": "Universidad Tecnologica Nacional",
        "college": "",
        "country": "AR",
        "degree": "Studied Electromechanical Engineering"
    }
]
#621-650
d650=[
    {
        "text": "Universidad de Barcelona, MD, 1990",
        "name": "Universidad de Barcelona",
        "college": "",
        "country": "ES",
        "degree": "MD"
    },
    {
        "text": "University of Sydney BS",
        "name": "University of Sydney",
        "college": "",
        "country": "AU",
        "degree": "B.S."
    },
    {
        "text": "1962 doctorate at the Helsinki University of Technology",
        "name": "Helsinki University of Technology",
        "college": "",
        "country": "FI",
        "degree": "Doctorate"
    },
    {
        "text": "B.S. University of California - San Diego, 1988",
        "name": "University of California - San Diego",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "Boston University, Boston, MA PhD 1992-1995 Biomedical Engineering",
        "name": "Boston University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Biomedical Engineering"
    },
    {
        "text": "Arizona State University Ph.D. Engineering Science Harvard University 1988.06",
        "name": "Arizona State University",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Engineering Science"
    },
    {
        "text": "Bachelor of Arts (Honours), University of Oxford1976",
        "name": "University of Oxford",
        "college": "",
        "country": "GB",
        "degree": "B.A. (Honours)"
    },
    {
        "text": "1993-1995 Doctorate Dr. rer. nat., University of Bayreuth and University of South",
        "name": "University of Bayreuth",
        "college": "",
        "country": "DE",
        "degree": "Dr. rer. nat."
    },
    {
        "text": "1984 to 1990 , Ph.D. Biochemistryx, Université de Genève Faculté des Sciences",
        "name": "Université de Genève",
        "college": "Faculté des Sciences",
        "country": "CH",
        "degree": "Ph.D. in Biochemistry"
    },
    {
        "text": "1983 - Diploma di \"Specialista in Ricerca Farmacologica\", Scuola di Formazione Professionale in Ricerche Farmacologiche della Regione Lombardia.",
        "name": "Scuola di Formazione Professionale in Ricerche Farmacologiche della Regione Lombardia",
        "college": "",
        "country": "IT",
        "degree": "Diploma in Ricerca Farmacologica"
    },
    {
        "text": "BS Pennsylvania State University 1968",
        "name": "Pennsylvania State University",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "Ph.D. (1972) and M.S. (1971)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D. and M.S."
    },
    {
        "text": "Ph.D: University of Pittsburgh, Crystallography/Biochemistry, 1970.",
        "name": "University of Pittsburgh",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Crystallography/Biochemistry"
    },
    {
        "text": "BA in Applied Biology at the University of Cambridge",
        "name": "University of Cambridge",
        "college": "",
        "country": "GB",
        "degree": "B.A. in Applied Biology"
    },
    {
        "text": "1970s BS Northwestern University",
        "name": "Northwestern University",
        "college": "",
        "country": "US",
        "degree": "B.S."
    },
    {
        "text": "medical degree at VU University Medical Center in 1988",
        "name": "VU University Medical Center",
        "college": "",
        "country": "NL",
        "degree": "Medical Degree"
    },
    {
        "text": "University of Nebraska Medical Center, Omaha, NE, MD, (1973)",
        "name": "University of Nebraska Medical Center",
        "college": "",
        "country": "US",
        "degree": "MD"
    },
    {
        "text": "BA Chemistry, Hope College, 1980 - 1984",
        "name": "Hope College",
        "college": "",
        "country": "US",
        "degree": "B.A. in Chemistry"
    },
    {
        "text": "Ph.D. Developmental Psychology, University of Virginia, 1986",
        "name": "University of Virginia",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Developmental Psychology"
    },
    {
        "text": "M.A. Developmental Psychology, University of Virginia, 1985",
        "name": "University of Virginia",
        "college": "",
        "country": "US",
        "degree": "M.A. in Developmental Psychology"
    },
    {
        "text": "B.S. Psychology, Michigan State University, 1980",
        "name": "Michigan State University",
        "college": "",
        "country": "US",
        "degree": "B.S. in Psychology"
    },
    {
        "text": "April 1965 - June 1969 Université de Montréal Doctor of Medicine",
        "name": "Université de Montréal",
        "college": "",
        "country": "CA",
        "degree": "Doctor of Medicine"
    },
    {
        "text": "Ph.D. Engineering Science (minor physics), California Institute of Technology, 1965 (Oct. 1964)",
        "name": "California Institute of Technology",
        "college": "",
        "country": "US",
        "degree": "Ph.D. in Engineering Science"
    },
    {
        "text": "Ph.D., University of California - San Diego 1986",
        "name": "University of California - San Diego",
        "college": "",
        "country": "US",
        "degree": "Ph.D."
    },
    {
        "text": "MB, ChB, University of Glasgow School of Medicine, 1984",
        "name": "University of Glasgow School of Medicine",
        "college": "",
        "country": "GB",
        "degree": "MB, ChB"
    },
    {
        "text": "1983 - 1988 Student in Chemistry at LMU Munich",
        "name": "LMU Munich",
        "college": "",
        "country": "DE",
        "degree": "Student in Chemistry"
    },
    {
        "text": "1983 - 1987 Princeton University Major field: Psychology B.A., Magna Cum Laude",
        "name": "Princeton University",
        "college": "",
        "country": "US",
        "degree": "B.A. in Psychology"
    },
    {
        "text": "Harpur College, State University of New York B.A., 1961, Biology",
        "name": "Harpur College, State University of New York",
        "college": "",
        "country": "US",
        "degree": "B.A. in Biology"
    },
    {
        "text": "1977-09-01 to 1981-06-01 , PhD (Psychology)",
        "name": "",
        "college": "",
        "country": "",
        "degree": "Ph.D. in Psychology"
    },
    {
        "text": "B.A. (Immunology and Neurobiology), Cornell University, 1971",
        "name": "Cornell University",
        "college": "",
        "country": "US",
        "degree": "B.A. in Immunology and Neurobiology"
    },
    {
        "text": "doctorat à l’Université de Caen",
        "name": "Université de Caen",
        "college": "",
        "country": "FR",
        "degree": "Doctorat"
    }
]
#66






