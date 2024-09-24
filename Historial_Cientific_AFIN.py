#!/usr/bin/env python3


from bibliografia.actions import (
    show_server_collections,
    download_collections,
    show_collections,
    download_collection,
    get_items,
    get_collections_reg0,
    write_collection,
)

# help("historial")

# show_server_collections()
# download_collections()

# exit()

# show_collections()

collection = []

# collection.extend(
#     [
#         "UWPY76KY",
#         "442HYH2P",
#         "2QEDV4YS",
#         "YPAJSHFV",
#         "R42QPUFI",
#         "36U9M8UA",
#         "N7K6GRL2",
#         "PWH78LJ5",
#     ]
# )


collection.append("UWPY76KY")  # indexed articles
collection.append("442HYH2P")  # articles
collection.append("2QEDV4YS")  # books
collection.append("YPAJSHFV")  # book chapter
collection.append("R42QPUFI")  # conference paper
collection.append("36U9M8UA")  # current projects
collection.append("N7K6GRL2")  # previos projects
collection.append("BRL62EC2")  # Competitive Transfer Grants
collection.append("PWH78LJ5")  # thesis: Non-competitive projects-agreements
collection.append("IARNE42E")  # Org International Conferences and Workshops
collection.append("FYCMV3HK")  # report: Participation in International Networks
collection.append("Q5E6D3QA")  # report: International stages
collection.append("H9FYFWQY")  # thesis: Completed doctoral theses
collection.append("YUGQZ453")  # thesis: Doctoral thesis in progress
collection.append("PJNPKBEK")  # thesis: Final Master Theses
collection.append("3HN4HS2I")  # Post-Doctoral Grants
collection.append("TZFYNY2Y")  # Pre-Doctoral Grants
collection.append("BW926N6F")  # AFIN free monthly publication
collection.append("364GBY9U")  # Workshops and other dissemination activities
collection.append("QR2SVS4L")  # Podcasts
collection.append("H4IXXNVT")  # TV presentations
collection.append("P5RR9R5K")  # Magazine Articles
collection.append("ARXRRBMK")  # Blog Posts

for item in collection:

    # download_collection(item)
    # get_collections_reg0(item, False)
    # get_collection(item, False)
    # get_items(item, False)
    get_items(item, True)

    # write_collection(item, True)
