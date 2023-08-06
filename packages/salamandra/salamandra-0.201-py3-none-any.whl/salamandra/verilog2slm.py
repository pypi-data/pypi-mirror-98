from salamandra.lexer import Lexer
import sys, os
sys.path.append(os.path.abspath('..'))
import re
from .net import Net
from .bus import Bus
from .input import Input
from .output import Output
from .inout import Inout
from .component import Component


def get_verilog_tokens(is_std_cell=False):
    # return tokens for lexer to run with this
    verilog_tokens = {
        'root': [
            (r'\s*module\s+([\w$]+|\\\S+\s)\s*(?:\((?:[\w$]+|\\\S+\s|,|\s*)*\))?\s*;\s*', 'module', 'module'),
            (r'\s*/\*.*?\*/\s*', None),
            (r'//#+(.*)\n', 'metacomment'),
            (r'\s*//.*\n', None),
            (r'`.*\n', None),
            (r'\s*\(\s*\*[\s\S]*?\*\s*\)\s*', None),  # (*...*)
        ],
        'module': [
            (r'\s*\(\s*\*[\s\S]*?\*\s*\)\s*', None),  # (*...*)
            (r'\s*//.*\n', None),  # //...
            (r'\s*assign\s+', 'assign_start', 'assignments'),  # assign
            (r'\s*else\s+if\s+\([\S\s]*?\)\s[\S\s]*?;\s*', 'check'),  # else if (...) ...;
            (r'\s*function\s+[\S\s]*?endfunction\s*', None),  # function ... endfunction
            (r'\s*(input|inout|output)(\s+signed)?(?:\s+\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\])?\s+([\w$]+|\\\S+\s)\s*;\s*', 'module_port'),
            # (input) (signed)? [(31):(0)]? (A);
            (r'\s*(input|inout|output)(\s+signed)?(?:\s+\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\])?\s+([\w$]+|\\\S+\s)\s*,\s*', 'module_port',
             'type_cont'),
            # (input) (signed)? [(31):(0)]? (A),
            (r'\s*wire(\s+signed)?(?:\s+\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\])?\s+([\w$]+|\\\S+\s)\s*;\s*', 'module_wire'),
            # wire (signed)? [(31):(0)]? (A);
            (r'\s*wire(\s+signed)?(?:\s+\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\])?\s+([\w$]+|\\\S+\s)\s*,\s*', 'module_wire', 'type_cont'),
            # wire (signed)? [(31):(0)]? (A),
            (r'\s*((?:[\w$]+|\\\S+)\s+(?:[\w$]+|\\\S+\s)\s*\([\S\s]*?\)\s*;\s*)', 'instance'),
            # (\mux$ i_mux(...);)
            (r'/\*.*?\*/', None),
            (r'//#\s*{{(.*)}}\n', 'section_meta'),
            (r'\s*endmodule\s*', 'end_module', '#pop'),
        ],
        'type_cont': [
            (r'\s*([\w$]+|\\\S+\s)\s*,?\s*', 'type_cont'),
            # (A),?
            (r'\s*,\s*', None),  # ,
            (r'\s*;\s*', None, '#pop'),  # ;
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'instance_ports': [
            # connect one thing
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{?\s*}?\s*\)\s*,?\s*', 'empty_pin'),  # .I(),? {}? -> I
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{?\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*}?\s*\)\s*,?\s*', 'connect_gnets'),
            # .I(2'b01),? {}? -> I,2,b,01/xx
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{?\s*([\w$]+|\\\S+\s)\s*(?:\[\s*(-?\d+)\s*:?\s*(-?\d+)?\s*\])?\s*}?\s*\)\s*,?\s*',
             'connect'),
            # .I(A[2:0]) # .I(B),? # .I(A[2]),? {}? -> I,A,2?,0?
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{?\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+\s)\s*}\s*}\s*}?\s*\)\s*,?\s*', 'connect_concat'),
            # .I({2{A}}) {}? -> I,2,A

            # connect many things
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,\s*', 'connect_many_gnets', 'bus_cont'),
            # .I({2'b01, -> I,2,b,01
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{\s*([\w$]+|\\\S+\s)\s*(?:\[\s*(-?\d+)\s*:?\s*(-?\d+)?\s*\])?\s*,\s*', 'connect_many',
             'bus_cont'),
            # .I({A, # .I({A[2:0], # .I({A[2], -> I,A,2?,0?
            (r'\s*\.([\w$]+|\\\S+\s)\s*\(\s*{s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+\s)\s*}\s*}\s*,\s*', 'connect_many_concat',
             'bus_cont'),  # .I({2{A}}, -> I,2,A

            (r'\s*,\s*', None),  # ,
            (r'\s*\)\s*;\s*', 'end_port', '#pop'),  # );
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'bus_cont': [
            (r'\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,?\s*', 'connect_many_gnets_cont'),  # 2'b01,? -> 2,b,01
            (r'\s*([\w$]+|\\\S+\s)\s*(?:\[\s*(-?\d+)\s*:?\s*(-?\d+)?\s*\])?\s*,?\s*', 'connect_many_cont'),
            # A,? # A[31:0],? # A[31],? -> A,2?,0?
            (r'\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+\s)\s*}\s*}\s*,?\s*', 'connect_many_concat_cont',),
            # {2{A}},? -> 2,A

            (r'\s*,\s*', None),  # ,
            (r'\s*}\s*\)\s*', 'end_bus', '#pop'),  # })
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
        ],
        'assignments': [
            (r'\s*{?\s*(\d+)\'([bodhBODH])([a-fA-F0-9x]+)\s*,?\s*}?\s*', 'assign_cont_gnet'),
            # 1'b0 / 13'h0 {}? ,? -> size,radix,val
            (r'\s*{?\s*{\s*(\d+)\s*{\s*([\w$]+|\\\S+\s)\s*}\s*}\s*,?\s*}?\s*', 'assign_cont_concat',),
            # {2{A}}  {}? ,?  -> 2,A
            (r'\s*{?\s*([\w$]+|\\\S+\s)\s*(?:\[\s*(-?\d+)\s*:?\s*(-?\d+)?\s*\])?\s*,?\s*}?\s*', 'assign_cont_net'),
            # A\A[12]\A[12:0] {}? ,? -> A,12?,0?
            (r'\s*}\s*', None),
            (r'\s*,\s*', None),
            (r'\s*=\s*', 'assign_eq'),
            (r'\s*;\s*', 'assign_finish', '#pop'),
            (r'//.*\n', None),
            (r'\s*/\*.*?\*/\s*', None),
            (r'[\S\s]*?;\s*', 'assign_break', '#pop'),  # not regular assign !danger!
        ],
    }
    if is_std_cell is True:
        verilog_tokens['module'][2] = (r'\s*((assign)|(else\s+if))\s+[\S\s]*?;\s*', None)  # assign/else if ... ; #?|(if)
        del verilog_tokens['module'][3]  # remove assign/else if
        del verilog_tokens['module'][6:8]  # remove wire and instances
    return verilog_tokens


def verilog2slm_file(fname, is_std_cell=False, implicit_wire=False, implicit_instance=False, verbose=False):
    '''Parse a named Verilog file

    Args:
      fname (str): File to parse.
      is_std_cell (bool): is STD cell (takes only I/O ports)
      implicit_wire (bool): add implicit wires
      implicit_instance (bool): guess instances if not exist
      verbose (bool): print warnings if exist
    Returns:
      List of parsed objects.
    '''
    # with open(fname, 'rb') as fh:
    #     text_ba = bytearray(fh.read())
    #     for i in range(len(text_ba)):
    #         if text_ba[i] is 0x80:
    #             text_ba[i] = 92
    #     text = text_ba.decode()
    with open(fname, 'rt') as fh:
        text = fh.read()

    return verilog2slm(text, is_std_cell, implicit_wire, implicit_instance, verbose)


def verilog2slm(text, is_std_cell=False, implicit_wire=False, implicit_instance=False, verbose=False):
    '''Parse a text buffer of Verilog code

    Args:
      text (str): Source code to parse
      is_std_cell (bool): is STD cell (takes only I/O ports)
      implicit_wire (bool): add implicit wires
      implicit_instance (bool): guess instances if not exist
      verbose (bool): print warnings if exist
    Returns:
      List of components objects.
    '''
    verilog_tokens_ = get_verilog_tokens(is_std_cell)  # get local verilog tokens
    lex = Lexer(verilog_tokens_)
    radix2bits = {'b': 2, 'o': 8, 'd': 10, 'h': 16}
    comp = None
    comps = []
    components = []
    text_subcomps = ''
    bus_cont = {}
    assign_dict = {}
    last_port_mode = None
    last_type = None

    re_com = re.compile(r'^(\\\S+)\s(\[(-?\d+)\])?$')
    for pos, action, groups in lex.run(text):  # run lexer and search for match
        groups = list(groups)
        for i, g in enumerate(groups):  # change "\name\n" to "\name "
            if g and g[0] == '\\':
                groups[i] = re.sub(re_com, r'\1 \2', g)
        groups = tuple(groups)

        if action == 'module':  # initiate Component
            module_name = groups[0]
            if module_name in Component.all_components():
                if verbose:
                    print('Warning: component ' + module_name + ' already exist')
                comp = None
            else:
                comp = Component(module_name)
                if is_std_cell:
                    comp.set_is_physical(True)
                    comp.set_dont_write_verilog(True)
            text_subcomps = ''

        elif comp is None:
            continue

        elif action == 'module_port' or (action == 'type_cont' and last_type == 'port'):  # adding pin/pinbus
            if action == 'module_port':
                p_mode, signed, msb, lsb, p_name = groups
                last_type = 'port'
                last_port_mode = p_mode
                last_width = (msb, lsb)
                last_signed = signed
            else:
                p_name = groups[0]
                p_mode = last_port_mode
                msb, lsb = last_width
                signed = last_signed

            if p_mode == 'input':
                p_type = Input
            elif p_mode == 'output':
                p_type = Output
            elif p_mode == 'inout':
                p_type = Inout

            if msb is None:
                comp.add_pin(p_type(p_name))
            else:
                signed = False if signed is None else True
                msb, lsb = max(int(msb), int(lsb)), min(int(msb), int(lsb))
                comp.add_pinbus(Bus(p_type, p_name, (msb, lsb), signed=signed))

        elif action == 'module_wire' or (action == 'type_cont' and last_type == 'wire'):  # adding net/netbus
            if action == 'module_wire':
                signed, msb, lsb, n_name = groups
                last_type = 'wire'
                last_width = (msb, lsb)
                last_signed = signed
            else:
                n_name = groups[0]
                (msb, lsb) = last_width
                signed = last_signed

            if n_name in comp.net_names() or n_name in comp.netbus_names():  # in case its pin(pin_adds_net)
                continue
            if msb is None:
                comp.add_net(Net(n_name))
            else:
                signed = False if signed is None else True
                msb, lsb = max(int(msb), int(lsb)), min(int(msb), int(lsb))
                comp.add_netbus(Bus(Net, n_name, (msb, lsb), signed=signed))

        elif action == 'assign_start':  # adding assignment - start
            assign_dict = {'state': 'l', 'l_count': 0, 'r_count': 0, 'l_cases': [], 'r_cases': []}
            assign_pos = pos[0]

        # adding assignment - continue, divide to cases and save for later
        elif action in ['assign_cont_net', 'assign_cont_gnet', 'assign_cont_concat']:
            state = assign_dict['state']
            assign_dict[state+'_cases'].append((action[12:],) + groups)
            assign_dict[state+'_count'] += 1

        elif action == 'assign_eq':  # adding assignment - continue, read "=", so change state to right
            assign_dict['state'] = 'r'

        elif action == 'assign_break':  # can't understand assign command
            assign_command = re.match(r'\s*(assign[\S\s]*?;)', text[assign_pos:]).groups()[0]
            if verbose:
                print('Warning: skipped assign command "{}"'.format(assign_command))

        elif action == 'assign_finish':  # adding assignment - end, read ";", now can handle all the connectivity
            assign_dict['l_nets'] = []
            assign_dict['r_nets'] = []
            for s in ['l', 'r']:  # handle each case for itself and after that connect_nets
                for i in range(assign_dict[s+'_count']):  # loop over num of cases in the present state(left or right)
                    case = assign_dict[s+'_cases'][i][0]
                    if case == 'net':
                        _, net_name, msb, lsb = assign_dict[s+'_cases'][i]  # A,msb?,lsb?
                        if msb is None:
                            # check if net_name is bus
                            if net_name in comp.net_names():
                                assign_dict[s+'_nets'].append(comp.get_net(net_name))
                                is_bus = False
                            elif net_name in comp.netbus_names():
                                msb = comp.get_netbus(net_name).msb()
                                lsb = comp.get_netbus(net_name).lsb()
                                is_bus = True
                            else:
                                raise Exception('cannot find net [' + net_name + '] in component')
                        else:
                            lsb = msb if lsb is None else lsb
                            is_bus = True

                        if is_bus is True:
                            for bit in range(int(msb), int(lsb) - 1, -1):
                                assign_dict[s+'_nets'].append(comp.get_net('{0}[{1}]'.format(net_name, bit)))

                    elif case == 'gnet':
                        _, size, radix, value = assign_dict[s+'_cases'][i]  # 2,b,01/xx
                        if 'x' in value:
                            value_bin = value
                        else:
                            value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                            value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                        for bit in range(int(size)):
                            assign_dict[s+'_nets'].append(comp.get_net("1'b{}".format(value_bin[bit])))

                    elif case == 'concat':
                        _, num, net_name = assign_dict[s+'_cases'][i]  # 2,A
                        net = comp.get_net(net_name)
                        for j in range(int(num)):
                            assign_dict[s+'_nets'].append(net)

            # after we interpreted all the cases we can connect them
            if len(assign_dict['l_nets']) != len(assign_dict['r_nets']):
                raise Exception('cant do assign between two different sizes')
            for i in range(len(assign_dict['l_nets'])):
                comp.connect_nets(assign_dict['r_nets'][i], assign_dict['l_nets'][i])

        elif action == 'instance':  # save all instance connectivity for later
            text_subcomps += '\n'+groups[0]

        elif action == 'end_module':  # read "endmodule"
            comps.append((comp, text_subcomps))

    # instances connectivity part
    for comp, text_subcomps in comps:
        if text_subcomps:
            last_inst = None
            verilog_tokens_['module'][-4] = (r'\s*([\w$]+|\\\S+\s)\s*([\w$]+|\\\S+\s)\s*\(\s*', 'instance_start', 'instance_ports')  # to handle instances
            verilog_tokens_['module'][-1] = (r'\s*endmodule\s*', None)  # dont do #pop
            lex = Lexer(verilog_tokens_)
            for pos, action, groups in lex.run(text_subcomps, start='module'):  # run lexer and search for match
                groups = list(groups)
                for i, g in enumerate(groups):  # change "\name\n" to "\name "
                    if g and g[0] == '\\':
                        groups[i] = re.sub(re_com, r'\1 \2', g)
                groups = tuple(groups)

                if action == 'instance_start':  # adding new subcomponent
                    inst, inst_name = groups  # nand i_nand
                    if inst not in Component.all_components():
                        if not implicit_instance:
                            raise Exception('instance ' + inst + ' should be implemented in verilog file')
                        sub = Component(inst)  # if not existed create it(with flag implicit_instance)
                        sub.set_property('is_guessed', True)
                    else:
                        sub = Component.get_component_by_name(inst)
                    comp.add_subcomponent(sub, inst_name)
                    last_inst = inst_name
                    last_sub = sub
                    is_guessed = last_sub.get_property('is_guessed')

                elif action == 'empty_pin':
                    if implicit_instance and is_guessed and groups[0] not in list(last_sub.pin_names()) + list(last_sub.pinbus_names()):
                        sub_pin = groups[0]
                        last_sub.add_pin(Inout(sub_pin))

                elif action == 'connect_gnets':
                    sub_pin, size, radix, value = groups  # I,2,b,01/xx
                    if 'x' in value:
                        value_bin = value
                    else:
                        value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                        value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                    if size == '1':  # not bus
                        if implicit_instance and is_guessed and sub_pin not in last_sub.pin_names():
                            last_sub.add_pin(Inout(sub_pin))
                        comp.connect("1'b{}".format(value_bin), last_inst + '.' + sub_pin)
                    else:  # bus
                        if implicit_instance and is_guessed and sub_pin not in last_sub.pinbus_names():
                            last_sub.add_pinbus(Bus(Inout, sub_pin, int(size)))
                        for bit in range(int(size)):  # connect lsb to lsb and so on
                            comp.connect("1'b{}".format(value_bin[::-1][bit]), '{0}.{1}[{2}]'.format(last_inst, sub_pin, bit))

                elif action == 'connect':  # connect net/bus to pin/bus
                    sub_pin, net_name, msb, lsb = groups  # I,A,2?,0?
                    if msb is None:
                        # check if net_name is bus
                        if net_name in comp.net_names():  # net2pin/bus#1
                            if implicit_instance and is_guessed and sub_pin not in last_sub.pin_names():
                                last_sub.add_pin(Inout(sub_pin))
                            if sub_pin in last_sub.pin_names():
                                comp.connect(net_name, last_inst + '.' + sub_pin)
                            else:  # net to bus#1
                                comp.connect(net_name, last_inst + '.' + sub_pin + '[0]')
                            is_bus = False
                        elif net_name in comp.netbus_names():  # netbus2pin/bus
                            msb = comp.get_netbus(net_name).msb()
                            lsb = comp.get_netbus(net_name).lsb()
                            is_bus = True
                            if msb == lsb:  # bus#1
                                if implicit_instance and is_guessed and sub_pin not in last_sub.pin_names():
                                    last_sub.add_pin(Inout(sub_pin))
                                if sub_pin in last_sub.pin_names():  # bus#1 to pin
                                    comp.connect('{}[{}]'.format(net_name, msb), last_inst + '.' + sub_pin)
                                    is_bus = False
                        else:
                            raise Exception('cannot find net [' + net_name + '] in component')
                    else:
                        lsb = msb if lsb is None else lsb
                        if msb == lsb:  # in case were bus#1 to pin(or bus#1)
                            if implicit_instance and is_guessed and sub_pin not in last_sub.pin_names():
                                last_sub.add_pin(Inout(sub_pin))
                            if sub_pin in last_sub.pin_names():
                                comp.connect('{}[{}]'.format(net_name, msb), last_inst + '.' + sub_pin)
                                is_bus = False
                            else:  # in case of bus#1 to bus#1
                                is_bus = True
                        else:
                            is_bus = True

                    if is_bus is True:  # connect netbus to pinbus
                        msb, lsb = int(msb), int(lsb)
                        if implicit_instance and is_guessed and sub_pin not in last_sub.pinbus_names():
                            width = max(msb, lsb) - min(msb, lsb) + 1  # in case of A[1:3]
                            last_sub.add_pinbus(Bus(Inout, sub_pin, width))
                        msb2lsb = 1 if msb > lsb else -1
                        for i, bit in enumerate(range(lsb, msb + msb2lsb, msb2lsb)):
                            comp.connect('{0}[{1}]'.format(net_name, bit),
                                         '{0}.{1}[{2}]'.format(last_inst, sub_pin, i))

                elif action == 'connect_concat':
                    sub_pin, num, net_name = groups  # I,2,A
                    if implicit_instance and is_guessed and sub_pin not in last_sub.pinbus_names():
                        last_sub.add_pinbus(Bus(Inout, sub_pin, int(num)))
                    for i in range(int(num)):
                        comp.connect(net_name, '{0}.{1}[{2}]'.format(last_inst, sub_pin, i))

                elif action in ['connect_many', 'connect_many_gnets', 'connect_many_concat']:  # save connectivity for later
                    bus_cont['count_cases'] = 1
                    bus_cont['sub_pin'] = groups[0]
                    bus_cont['nets2sub'] = [(action,) + groups[1:]]

                elif action in ['connect_many_cont', 'connect_many_gnets_cont', 'connect_many_concat_cont']:  # save connectivity for later
                    bus_cont['count_cases'] += 1
                    bus_cont['nets2sub'].append((action[:-5],) + groups)

                elif action == 'end_bus':  # connect all connectivity above to pinbus
                    bus_connections = []  # save all connections (net,pin) and connect them at the end
                    pin_counter = 0
                    for d in range(bus_cont['count_cases']-1, -1, -1):  # from lsb to msb, end to start
                        if bus_cont['nets2sub'][d][0] == 'connect_many':  # connect net/bus to pin/bus
                            _, net_name, msb, lsb = bus_cont['nets2sub'][d]  # _,A,2,1?
                            if msb is None:
                                # check if net_name is bus
                                if net_name in comp.net_names():  # net2pinbus
                                    bus_connections.append((net_name, '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], pin_counter)))
                                    pin_counter += 1
                                    is_bus = False
                                elif net_name in comp.netbus_names():  # netbus2pinbus
                                    msb = comp.get_netbus(net_name).msb()
                                    lsb = comp.get_netbus(net_name).lsb()
                                    is_bus = True
                                elif implicit_wire is True:
                                    comp.add_net(Net(net_name))
                                    bus_connections.append((net_name, '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], pin_counter)))
                                    pin_counter += 1
                                    is_bus = False
                                else:
                                    raise Exception('cannot find net [' + net_name + '] in component')

                            else:
                                lsb = msb if lsb is None else lsb
                                is_bus = True

                            if is_bus is True:  # connect netbus to pinbus
                                p_c = pin_counter
                                for i, bit in enumerate(range(int(lsb), int(msb) + 1)):
                                    bus_connections.append(('{0}[{1}]'.format(net_name, bit),
                                                            '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], i + p_c)))
                                    pin_counter += 1

                        elif bus_cont['nets2sub'][d][0] == 'connect_many_gnets':
                            _, size, radix, value = bus_cont['nets2sub'][d]  # _,2,b,01/xx
                            if 'x' in value:
                                value_bin = value
                            else:
                                value_dec = int(value, radix2bits[radix.lower()])  # convert value to decimal
                                value_bin = bin(value_dec)[2:].zfill(int(size))  # convert value to binary padded to size

                            if size == '1':  # not bus
                                bus_connections.append(("1'b{}".format(value_bin),
                                                        '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], pin_counter)))
                                pin_counter += 1
                            else:  # bus
                                p_c = pin_counter
                                for bit in range(int(size)):  # connect lsb to lsb and so on
                                    bus_connections.append(("1'b{}".format(value_bin[::-1][bit]),
                                                            '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], bit + p_c)))
                                    pin_counter += 1

                        elif bus_cont['nets2sub'][d][0] == 'connect_many_concat':
                            _, num, net_name = bus_cont['nets2sub'][d]  # _,2,A
                            p_c = pin_counter
                            for i in range(int(num)):
                                bus_connections.append((net_name, '{0}.{1}[{2}]'.format(last_inst, bus_cont['sub_pin'], i + p_c)))
                                pin_counter += 1

                    if implicit_instance and is_guessed and bus_cont['sub_pin'] not in last_sub.pinbus_names():
                        last_sub.add_pinbus(Bus(Inout, bus_cont['sub_pin'], pin_counter))

                    for n, p in bus_connections:  # connect all connections above
                        comp.connect(n, p)

        components.append(comp)
    return components
