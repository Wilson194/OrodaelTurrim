from ZNS.User.UserFramework import IKnowledgeBase


class KnowledgeBase(IKnowledgeBase):
    def create_knowledge_base(self):
        print('Creating knowledge base')
        print(self.proxy.get_map_size)
