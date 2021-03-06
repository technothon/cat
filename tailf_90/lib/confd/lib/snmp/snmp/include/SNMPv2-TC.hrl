%%
%% %CopyrightBegin%
%%
%% Copyright Ericsson AB 2004-2009. All Rights Reserved.
%%
%% The contents of this file are subject to the Erlang Public License,
%% Version 1.1, (the "License"); you may not use this file except in
%% compliance with the License. You should have received a copy of the
%% Erlang Public License along with this software. If not, it can be
%% retrieved online at http://www.erlang.org/.
%%
%% Software distributed under the License is distributed on an "AS IS"
%% basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
%% the License for the specific language governing rights and limitations
%% under the License.
%%
%% %CopyrightEnd%
%%

%% This file was automatically generated by snmp_mib_to_hrl v3.0
%% Date: 22-Jan-2004::15:38:42

-ifndef('SNMPv2-TC').
-define('SNMPv2-TC', true).

-define(snmpv2TC, [1,3,6,1,6,3,0]).

%% Range values


%% Definitions from 'StorageType'
-define('StorageType_readOnly', 5).
-define('StorageType_permanent', 4).
-define('StorageType_nonVolatile', 3).
-define('StorageType_volatile', 2).
-define('StorageType_other', 1).

%% Definitions from 'RowStatus'
-define('RowStatus_destroy', 6).
-define('RowStatus_createAndWait', 5).
-define('RowStatus_createAndGo', 4).
-define('RowStatus_notReady', 3).
-define('RowStatus_notInService', 2).
-define('RowStatus_active', 1).

%% Definitions from 'TruthValue'
-define('TruthValue_false', 2).
-define('TruthValue_true', 1).

%% Default values

-endif.
