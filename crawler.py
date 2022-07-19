import requests
import csv


def requester(top=1000, skip=0):
    response = requests.post(
        "https://isbn-search-br.search.windows.net/indexes/isbn-index/docs/search?api-version=2016-09-01",
        headers={
            "api-key": "100216A23C5AEE390338BBD19EA86D29",
            "content-type": "application/json; charset=UTF-8",
        },
        json={
            "searchMode": "any",
            "searchFields": "Imprint",
            "queryType": "full",
            "search": "saraivajur",
            "top": top,
            "select": "Authors,Colection,Countries,Date,Imprint,Title,RowKey,PartitionKey,RecordId,FormattedKey,Subject,Veiculacao,Ano",
            "skip": skip,
            "count": True,
            "filter": "",
            "orderby": None,
            "facets": ["Imprint,count:50", "Authors,count:50"],
        },
    )

    if response.status_code == 200:
        return response.json().get("value")

    return None


def run():
    with open("SaraivaJur.csv", "w", encoding="utf-8", newline='') as cursor:
        writer = csv.DictWriter(
            cursor,
            fieldnames=[
                "@search.score",
                "PartitionKey",
                "RowKey",
                "Authors",
                "Date",
                "FormattedKey",
                "Imprint",
                "Subject",
                "Title",
                "Colection",
                "RecordId",
                "Countries",
                "Veiculacao",
                "Ano",
            ],
        )
        writer.writeheader()

        skip = 0
        top = 1000

        obras = requester(top=top, skip=skip)
        while obras:
            for obra in obras:
                writer.writerow(obra)

            skip += top
            obras = requester(top=top, skip=skip)

if __name__ == "__main__":
    run()
