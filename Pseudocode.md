importing various libraries and modules

defining constants
pygame window initalisation
custom events
accessing assets for game

class projectile:
    initalisation function:
        setting projectile attributes
    draw function:
        draw projectiles for player/enemy
    handle movement function:
        if player is hit:
             place the projectile again into enemy body
             reduce its health
        if enemy is hit:
             place the projectile back into player body
             remove the enemy from the set
        if next movement of projectile doesnt lead it outside window:
             continue movement of projectile
        else:
             place the projectile back into player/enemy body

class enemy:
    initalisation function:
        setting enemy attributes
        making an object bullet belonging to class projectile for enemy object
    draw function:
        draw the enemy cannon on the basis of player location

draw function:
    call global constants
    fill the background with an image
    draw player projectile
    draw projectile for every enemy in the set
    draw tank body on basis of current angle
    draw tank cannon on basis of current angle depending on location of  mouse
    draw player health
    draw kill count text on top left corner

movement function:
    call global constants

    if a is pressed:
        rotate the tank body in anticlockwise sense
    if d is pressed:
        rotate the tank body in clockwise sense
    if w is pressed:
        if the next movement of tank doesnt lead it outside the window:
            move it forward along the direction in which it is facing currently
   if s is pressed:
        if the next movement of tank doesnt lead it outside the window:
            move it backward along the direction in which it is facing currently
     call player's projectile handle movement function
     call enemy's projectile handle movement function for every enemy in set

main function:
    call global constant
    creating projectile object and an enemy set
    while True:
        if health of player is greater than 0:
            if total kill>=0:
                 create an enemy object
                 add object to enemy set
            if total kill>=5:
                 create an enemy object
                 add object to enemy set
            if total kill>=10:
                 create an enemy object
                 add object to enemy set
           if total kill>=15:
                 create an enemy object
                 add object to enemy set

           if lmb is pressed:
                 shoot projectile from player
          
           if any enemy belonging to set doesnt have active bullet on window:
                shoot bullet towards player
        else:
            draw game over menu with total kills
call main funtion
