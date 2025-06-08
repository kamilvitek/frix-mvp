#Conflict score
from app.services.eventbrite import EventbriteHandler
from app.models.event_storage import EventStorage
from app.models.conflicts import ConflictAnalyzer

###Simulation of user's input
class Customer_event:
    def __init__ (self, q, country, category, start, end, phq_label):
        self.q = q
        self.country = country
        self.category = category
        self.start = start
        self.end = end
        self.phq_label = phq_label
        # Generate a unique ID for the event
        self.id = f"{self.q}_{self.country}_{self.category}".lower().replace(" ", "_")
    
    def __str__(self):
        return(
            f"Customer_event = {self.q}\n"
            f"Country = {self.country}\n"
            f"Start = {self.start}, End={self.end}\n"
            f"Phq_label = {self.phq_label}\n"
        )

    def get_related_events(self):
        """
        Fetch and store related events for this customer event
        """
        eventbrite = EventbriteHandler()
        storage = EventStorage()
        
        # First try to get events from storage
        events = storage.get_related_events(self.id)
        
        # If no events found in storage, fetch from Eventbrite and store them
        if not events:
            events = eventbrite.search_related_events(self)
            if events:
                storage.store_related_events(self.id, events)
        
        return events

input_event = Customer_event("Colors of Ostrava", "Czechia", "conferences", "", "", "financial-services")

# Example usage:
# related_events = input_event.get_related_events()

#Potřebuju se naučit ty date formáty, abych věděl, co tam mám napsat. 
#Potom potřebuju na základě těchto údajů všech údajů v "input_event" nahrát další eventy pomocí api, které s tím souvisí
#Pořebuju udělat decupling
#Potom potřebuju vypočítat conflict-score

