# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:48:13 2020

@author: ThomasBitskyJr
(C) Copyright 2020 Automated Design Corp. All Rights Reserved.

A simple one-to-many pub/sub class for supporting global events
and loose coupling of APIs. Uses asyncio for non-blocking publication
of events. 

Adapted from basicevents by agalera
Licensed under the GPL.
"""


"""
Important!
Disable ctrl-c causing an exception and blocking graceful shutdown.
"""
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'


import asyncio
import logging
import time
#import traceback
from typing import AnyStr, Callable

class Events(object):
    """A simple one-to-many pub/sub class for supporting global events.
    Requires asyncio
    
    @Usage:
        
        Asynchronous:
        
        @Events.subscribe("hello")
        async def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)
        
        @Events.subscribe("hello")
        async def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)
            
        Events.publish("hello", "There")
        
        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}
        
        
        Blocking:
        @Events.subscribe("hello")
        def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)
        
        @Events.subscribe("hello")
        def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)
            
        Events.publishSync("hello", "There")
        
        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}            
            
        
    """
    
    
    subs = {}


    @staticmethod
    def add_subscribe(event:str, func):
        if event not in Events.subs:
            Events.subs[event] = []

        loop = asyncio.get_event_loop()
        Events.subs[event].append({"func": func, "loop": loop})

    @staticmethod
    def unsubscribe_method(event:str, func:Callable) -> None:
        """Remove the subscription on a topic for a particular
        function.
        """
        if event in Events.subs:

            newlist = []

            for item in Events.subs[event][:]:
                if "func" in item:
                    if item["func"] != func:
                        newlist.append(item)

            Events.subs[event] = newlist

    



        



    @staticmethod
    def subscribe_method(event:str, func:Callable) -> None:
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event : str
            ID of the event
            
        func : function        
            The method/slot to call back. 
        """
        Events.add_subscribe(event,func)

    @staticmethod
    def subscribe(event:str) -> None:
        """Subscribe a function  to an event ID. 
        
        Parameters
        ----------
        event : str
            ID of the event
                
        """
               
        def wrap_function(func:Callable):

            Events.add_subscribe(event, func)
            return func
        return wrap_function


    @staticmethod
    def publish(event:str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. 
        
        For coroutine functions defined with async, returns immediately. The
            callback is scheduled into the event loop.
        Synchronous functions are executed in order and block untile done.
        """


        if event in Events.subs:

            try:
                for ev in Events.subs[event]:

                    if asyncio.iscoroutinefunction(ev["func"]):
                        
                        loop = ev["loop"] #asyncio.get_event_loop()

                        try:
                            asyncio.run_coroutine_threadsafe(ev["func"](*args, **kwargs), loop)
                        except Exception as e:
                            logging.warning(f"Exception calling {event} async callback: {e}")                        

                    else:

                        try:
                            ev["func"](*args, **kwargs)
                        except Exception as e:
                            logging.warning(f"Exception calling {event} synchronous callback: {e}")       

            except Exception as e:
                logging.warning(f"Exception processing event {event} :\n {e}")   
        
        
    @staticmethod
    def publishSync(event:str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. SYNCHRNOUS AND BLOCKING.
        
        """
        try:
            for ev in Events.subs[event]:
                try:
                    ev["func"](*args, **kwargs)
                except Exception as e:
                    Events.logger(f"{e}")
        except:
            pass
        
        
"""
# avoids having to import Events
add_subscribe = Events.add_subscribe
subscribe = Events.subscribe
send = Events.send
send_queue = Events.send_queue
send_thread = Events.send_thread
send_blocking = Events.send_blocking
"""
    



if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe("testsig")
    async def testsig_decorator(data):
        print(f"Decorator Test signal received! {data}")

    async def testsig_method(data):
        print (f"Method test signal received! {data}")


    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        print ("Test signal to multiple methods.")
        Events.subscribe_method("testsig", testsig_method)

        time.sleep(0.5)

        Events.publish("testsig", "First")

        time.sleep(0.5)

        print ("Test removing method.")
        Events.unsubscribe_method("testsig", testsig_method)
        Events.publish("testsig", "Second")

        print( "Press CTRL-C to stop.")  

        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"Exception: {ex}")  
            
    finally:
        
        loop.stop()

        print( "Goodbye.")
