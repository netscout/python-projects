from game import Game

game = Game(
    caption="벽돌 깨기", 
    width=800, 
    height=600, 
    bg_image_filename='images/background.jpg', 
    frame_rate=60)

game.run()