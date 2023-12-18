import trio
from pyskyq import EPG, XMLTVListing
from datetime import datetime, timedelta

async def main():
    epg = EPG('192.168.1.30') # replace with hostname / IP of your Sky box
    await epg.load_skyq_channel_data() # load channel listing from Box.
    all_72_hour = XMLTVListing('http://www.xmltv.co.uk/feed/8943')
    async with trio.open_nursery() as nursery:
        nursery.start_soon(all_72_hour.fetch)
    epg.apply_XMLTVListing(all_72_hour)

    # Get the start and end times for the next 7 days
    start_time = datetime.now()
    end_time = start_time + timedelta(days=7)

    # Filter the EPG data to show the upcoming items
    upcoming_items = []
    for channel in epg.channels:
        for item in channel.items:
            if item.start_time >= start_time and item.start_time <= end_time:
                upcoming_items.append(item)

    # Print the upcoming items
    print('Upcoming items in the next 7 days:')
    for item in upcoming_items:
        print(f'{item.start_time.strftime("%Y-%m-%d %H:%M:%S")} - {item.title} on {channel.name}')

if __name__ == "__main__":
    trio.run(main)

