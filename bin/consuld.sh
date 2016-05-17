#!/bin/sh
/bin/consul agent -config-dir=/config -join $CONSUL -node $MAC
