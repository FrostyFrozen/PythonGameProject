# -*- coding: utf-8 -*-

  while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
            
            color w init
            
            #STARE
            
                   while len(self.platforms) < 6:
           
            width = random.randrange(50, 100)
            
            col_randomizer=rnd.randint(0,2)
            multiplier=1
            if (col_randomizer==0):
                col=YELLOW
            elif (col_randomizer==1):
                col=GREEN
            else:
                col=RED
            if self.score > 400:
                multiplier=0.9
            if self.score > 700:
                multiplier=0.8
                
            p = Platform(random.randrange(0, WIDTH-width),
                         random.randrange(-75, -30),
                         multiplier*width, 20,col)        
            self.platforms.add(p)
            self.all_sprites.add(p)