import datetime

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
from crbs.models import Room, Booking


# Create your views here.

class RoomList(View):
    def get(self, request):
        all_rooms = Room.objects.all()
        context = {}
        all_rooms_plus_bookings_list = []
        search_room_name = request.GET.get("search_room_name")
        search_min_cap = request.GET.get("search_min_cap")
        search_projector = request.GET.get("search_projector")
        print(search_min_cap)
        print(search_room_name)
        print(search_projector)
        if search_room_name:
            all_rooms = all_rooms.filter(name__icontains=search_room_name)
        if search_min_cap:
            all_rooms = all_rooms.filter(capacity__gte=search_min_cap)
        if search_projector:
            all_rooms = all_rooms.filter(projector=True)

        for room in all_rooms:
            bookings = Booking.objects.filter(room_id=room.id)
            room_dates = []
            for booking in bookings:
                room_dates.append(booking.date)
            room_plus_bookings = {"room": room, "bookings": room_dates}
            all_rooms_plus_bookings_list.append(room_plus_bookings)

        context["rooms_and_bookings"] = all_rooms_plus_bookings_list
        context["today"] = datetime.date.today()

        return render(request, "room_list.html", context)


class AddRoom(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST["name"]
        capacity = request.POST["capacity"]
        projector = False
        if "projector" in request.POST.keys():
            projector = True

        if Room.objects.all().filter(name=name):
            my_response = HttpResponse()
            my_response.write("Ten pokój już istnieje")
            return my_response

        if name != '' and name is not None and capacity and int(capacity) > 0:
            my_response = HttpResponseRedirect("/room-list")
            new_room = Room()
            new_room.name = name
            new_room.capacity = capacity
            new_room.projector = projector
            new_room.save()
            return my_response
        else:
            my_response = HttpResponse()
            my_response.write("Data incorrect")
            return my_response


class ModifyRoom(View):
    def get(self, request, room_id):
        room_name = Room.objects.get(pk=room_id).name
        room_capacity = Room.objects.get(pk=room_id).capacity
        room_projector = ""
        if Room.objects.get(pk=room_id).projector:
            room_projector = "checked"
        context = {"room_name": room_name, "room_capacity": room_capacity, "room_projector": room_projector}
        return render(request, "modify_room.html", context)

    def post(self, request, room_id):
        name = request.POST["name"]
        capacity = request.POST["capacity"]
        projector = False
        if "projector" in request.POST.keys():
            projector = True

        if Room.objects.all().filter(pk=room_id):
            pass
        else:
            my_response = HttpResponse()
            my_response.write("Ten pokój nie istnieje")
            return my_response

        if name != '' and name is not None and capacity and int(capacity) > 0:
            my_response = HttpResponseRedirect("/room-list")
            new_room = Room.objects.get(pk=room_id)
            new_room.name = name
            new_room.capacity = capacity
            new_room.projector = projector
            new_room.save()
            return my_response
        else:
            my_response = HttpResponse()
            my_response.write("Data incorrect")
            return my_response


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return HttpResponseRedirect("/room-list")


class BookRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        bookings = Booking.objects.filter(room_id=room.id)
        room_dates = []
        for booking in bookings:
            room_dates.append(booking.date)
        context = {"room": room, "bookings": room_dates}
        return render(request, "book_room.html", context)

    def post(self, request, room_id):
        comment = request.POST["comment"]
        date = datetime.datetime.strptime(request.POST["date"], '%Y-%m-%d').date()
        bookings = Booking.objects.filter(room_id=room_id)
        room_dates = []
        for booking in bookings:
            room_dates.append(booking.date)
        if date in room_dates:
            my_response = HttpResponse()
            my_response.write("Pokój jest zajęty tego dnia")
            return my_response
        elif date < datetime.date.today():
            my_response = HttpResponse()
            my_response.write("Data z przeszłości")
            return my_response
        else:
            new_booking = Booking()
            new_booking.room_id = room_id
            new_booking.comment = comment
            new_booking.date = date
            new_booking.save()
            return HttpResponseRedirect("/room-list")


class RoomDetails(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        context = {}

        bookings = Booking.objects.filter(room_id=room.id).order_by("date")

        room_plus_bookings = {"room": room, "bookings": bookings}

        context["room_and_bookings"] = room_plus_bookings

        # my_response.write(all_rooms_dict)
        # return my_response
        return render(request, "room_details.html", context)
