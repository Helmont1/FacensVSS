#ifndef REFEREECLIENT_H
#define REFEREECLIENT_H

#include "../client.h"
#include "../../include/vssref_command.pb.h"

class RefereeClient : public Client
{
public:
    using Client::Client;

    // Internal getters
    VSSRef::Foul getLastFoul();
    VSSRef::Color getLastFoulColor();
    VSSRef::Quadrant getLastFoulQuadrant();
    VSSRef::Color getLastGoalColor();

private:
    // Environment management
    std::tuple<VSSRef::Foul, VSSRef::Color, VSSRef::Quadrant> _lastFoulData;
    std::tuple<VSSRef::Color> _lastGoalData;
    QReadWriteLock _foulMutex;
    QReadWriteLock _goalMutex;

    // Network management
    void connectToNetwork();
    void disconnectFromNetwork();

    // Internal run
    void runClient();
};

#endif // REFEREECLIENT_H
