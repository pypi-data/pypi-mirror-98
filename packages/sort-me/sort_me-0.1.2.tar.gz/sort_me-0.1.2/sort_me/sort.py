import bubble
import insertion
import selection
import quick
import merge
class sort:

    def __init__(self):
        pass

    def bubble(self, lst):
        return bubble.bubble(lst)

    def insertion(self, lst):
        return insertion.insertion(lst)

    def selection(self, lst):
        return selection.selection(lst)

    def quick(self, lst):
        return quick.quick(lst)

    def merge(self, lst):
        return merge.merge(lst)