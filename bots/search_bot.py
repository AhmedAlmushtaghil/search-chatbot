# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

def query_func(search_query):
    
    endpoint = "https://chatbotsearchservice.search.windows.net/"
    admin_key = "4CF0B5C911347AE7BBCBF5B3B8D9212C"
    index_name = "hotels-sample-index"
    
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(admin_key))

    features = {
        "search_fields":"HotelName",
        "select":"HotelName, Rating",
        "filter":"Rating gt 4",
        "order_by":"Rating desc"}

    query_result = search_client.search(
                            include_total_count=True,
                            search_text=f"{search_query}", 
                            search_fields=f"{features['search_fields']}", 
                            select=f"{features['select']}", 
                            filter=f"{features['filter']}", 
                            order_by=f"{features['order_by']}")

    return query_result

class SearchBot(ActivityHandler):
    
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        
        message = []
        results = query_func(turn_context.activity.text)
        for result in results:
                message.append(f"{result['HotelName']} has a rating of {result['Rating']}")
        
        output_message = "\n\n".join(message)
        await turn_context.send_activity(MessageFactory.text(output_message))