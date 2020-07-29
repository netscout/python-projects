from pygame.rect import Rect

class GameObject:
    def __init__(self, x, y, w, h, speed=(0,0)):
        #left, top, width, height
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery
    
    def _left_egde(self):
        """
        충돌 검사를 위한 오브젝트의 왼쪽 면
        """
        return Rect(self.left, self.top, 1, self.height)

    def _right_egde(self):
        """
        충돌 검사를 위한 오브젝트의 오른쪽 면
        """
        return Rect(self.right, self.top, 1, self.height)

    def _top_egde(self):
        """
        충돌 검사를 위한 오브젝트의 위쪽 면
        """
        return Rect(self.left, self.top, self.width, 1)

    def _bottom_egde(self):
        """
        충돌 검사를 위한 오브젝트의 아랫쪽 면
        """
        return Rect(self.left, self.bottom, self.width, 1)

    @property
    def edges(self):
        return dict(
            left = self._left_egde(),
            right = self._right_egde(),
            top = self._top_egde(),
            bottom = self._bottom_egde()
        )


    def draw(self, surface):
        """
        자식 클래스에서 처리하도록 비워둠
        """
        pass

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)
    
    def update(self):
        if self.speed == [0, 0]:
            return

        #*연산자는 리스트를 튜플 형태로 전달
        #**연산자는 딕셔너리 형태로 전달
        self.move(*self.speed)
