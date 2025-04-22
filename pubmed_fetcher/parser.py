# pubmed_fetcher/parser.py
import re
from typing import Dict
import xml.etree.ElementTree as ET

COMPANY_KEYWORDS = ["pharma", "biotech", "therapeutics", "laboratories", "inc", "corp"]

def parse_article(xml_data: str) -> Dict[str, str]:
    result = {
        "PubmedID": "N/A",
        "Title": "N/A",
        "Publication Date": "N/A",
        "Non-academic Author(s)": "",
        "Company Affiliation(s)": "",
        "Corresponding Author Email": ""
    }

    try:
        xml_data = "<PubmedArticle>" + xml_data
        root = ET.fromstring(xml_data)

        pmid = root.findtext(".//PMID")
        title = root.findtext(".//ArticleTitle")
        pubdate = root.findtext(".//PubDate/Year") or "Unknown"

        result["PubmedID"] = pmid or "N/A"
        result["Title"] = title or "N/A"
        result["Publication Date"] = pubdate

        company_authors = []
        companies = []
        emails = []

        for author in root.findall(".//Author"):
            aff = author.findtext("AffiliationInfo/Affiliation") or ""
            email = extract_email(aff)

            if is_company_affiliation(aff):
                name = f"{author.findtext('ForeName')} {author.findtext('LastName')}".strip()
                company_authors.append(name)
                companies.append(aff)
                if email:
                    emails.append(email)

        result["Non-academic Author(s)"] = "; ".join(company_authors)
        result["Company Affiliation(s)"] = "; ".join(set(companies))
        result["Corresponding Author Email"] = emails[0] if emails else ""

    except Exception as e:
        result["Title"] = f"Error parsing: {str(e)}"

    return result

def is_company_affiliation(aff: str) -> bool:
    return any(keyword.lower() in aff.lower() for keyword in COMPANY_KEYWORDS)

def extract_email(text: str) -> str:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
    return match.group(0) if match else ""
