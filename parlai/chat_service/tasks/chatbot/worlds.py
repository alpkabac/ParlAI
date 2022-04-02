#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# py parlai/chat_service/tasks/overworld_demo/run.py --debug --verbose
import os.path
import sys

from parlai.chat_service.services.messenger.worlds import OnboardWorld
from parlai.core.agents import create_agent_from_shared
from parlai.core.worlds import World
from parlai.chat_service.services.websocket.firebase import get_history, create_user, set_history 


# ---------- Chatbot demo ---------- #
class MessengerBotChatOnboardWorld(OnboardWorld):
    """
    Example messenger onboarding world for Chatbot Model.
    """

    @staticmethod
    def generate_world(opt, agents):
        return MessengerBotChatOnboardWorld(opt=opt, agent=agents[0])

    def parley(self):
        self.episodeDone = True


class MessengerBotChatTaskWorld(World):
    """
    Example one person world that talks to a provided agent (bot).
    """

    MAX_AGENTS = 1
    # MODEL_KEY = 'blender_90M'
    # MODEL_KEY = 'blender3B_1024'
    MODEL_KEY = 'blenderbot'

    def __init__(self, opt, agent, bot):
        self.agent = agent
        self.episodeDone = False
        self.model = bot
        self.first_time = True
        global userid
        self.userid = userid
        global history
        self.history = history

    @staticmethod
    def generate_world(opt, agents):
        if opt['models'] is None:
            raise RuntimeError("Model must be specified")
        return MessengerBotChatTaskWorld(
            opt,
            agents[0],
            create_agent_from_shared(
                opt['shared_bot_params'][MessengerBotChatTaskWorld.MODEL_KEY]
            ),
        )

    @staticmethod
    def assign_roles(agents):
        agents[0].disp_id = 'ChatbotAgent'
        
    def parley(self):
        if self.first_time:
            self.first_time = False
            if history is not None:
                self.load_history_from_database()
        a = self.agent.act()
        if a is not None:
            if '[DONE]' in a['text']:
                self.episodeDone = True
            elif '[RESET]' in a['text']:
                self.model.reset()
                self.agent.observe({"text": "[History Cleared]", "episode_done": False})
            elif '[HISTORY]' in a['text']:
                    current_history = str(self.model.history.get_history_str())    
                    self.agent.observe({"text": current_history , "episode_done": False})
            elif '[PERSONA]' in a['text']:
                    a['text'] = a['text'].replace('[PERSONA]\n', "")
                    self.model.observe({"text": a['text'], "episode_done": False})
                    #print(self.model.persona) check later with self.model.model.persona
            elif '[SAVE]' in a['text']:
                    self.save_history()
            elif '[LOAD]' in a['text']:
                    self.load_history(a['text'].replace('[LOAD]', ""))
            elif '[EDIT]' in a['text']:
                    a['text'] = a['text'].replace('[EDIT]', "")
                    self.add_history(a['text'])
            else:
                print("===act====")
                print(a)
                print("~~~~~~~~~~~")
                self.model.observe(a)
                response = self.model.act()
                print("===response====")
                print(response)
                print("~~~~~~~~~~~")
                current_history = str(self.model.history.get_history_str())    
                 #print model memories
                # print("===history====")
                # print(self.model.model.long_term_memory.memory_dict)
                # print("==============")
                self.agent.observe({'text': response['text'], 'history': current_history, 'episode_done': False})

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown()
    
    def save_history(self):
        set_history(self.userid, self.model.history.get_history_str())

    def load_history(self, text):
        self.model.reset()
        self.model.observe({"text": text, "episode_done": False})
    
    def add_history(self, text):
        history = self.model.history.get_history_str() + '\n' + text
        self.model.reset()
        self.model.observe({"text": history, "episode_done": False})
    
    def load_history_from_database(self):
        self.history = get_history(self.userid)
        self.model.observe({"text": self.history, "episode_done": False})

# ---------- Overworld -------- #
class MessengerOverworld(World):
    """
    World to handle moving agents to their proper places.
    """

    def __init__(self, opt, agent):
        self.agent = agent
        self.opt = opt
        self.first_time = True
        self.episodeDone = False

    @staticmethod
    def generate_world(opt, agents):
        return MessengerOverworld(opt, agents[0])

    @staticmethod
    def assign_roles(agents):
        for a in agents:
            a.disp_id = 'Agent'

    def episode_done(self):
        return self.episodeDone
    
    def parley(self):
        if self.first_time:
            self.first_time = False
        a = self.agent.act()
        if a is not None:
            self.episodeDone = True
            global userid
            userid = a['text']
            global history
            history = get_history(userid)
            print("===history====")
            print(history)
            print("==============")
            # if history is not None:
            #     MessengerBotChatTaskWorld().load_history()
            return 'default'
