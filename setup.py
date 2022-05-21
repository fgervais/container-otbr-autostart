import dbus


bus = dbus.bus.BusConnection("unix:path=/run/dbus/system_bus_socket")

for service in bus.list_names():
    print(service)

