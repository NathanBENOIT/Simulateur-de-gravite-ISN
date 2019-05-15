# -*- coding: utf-8 -*-

import arcade
import pymunk
import timeit
import math
import os

LargeurEcran = 1920
HauteurEcran = 1080
Titre = "Simulateur de gravité"

#Définition des formes physiques
class Physique(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape

#Définition des caractéristiques des formes physiques
class Formes(Physique):
    def __init__(self, pymunk_shape, filename, width, height):
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height

class Simulation(arcade.Window):
    #Définition de la simulation

    #Initialsiation
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
        # Définition de l'image de fond à l'ouverture du programme
        self.background = None
        self.background = arcade.load_texture("images/Terre.jpg")

        # Définition de l'espace physique pymunk et ses caractéristiques
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)

        # Liste des sprites et lignes
        self.sprite_list = arcade.SpriteList()
        self.static_lines = []

        # Pour déplacer les objets
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.draw_time = 0
        self.processing_time = 0
        
        # Définition de l'objet et de l'astre définis de base
        self.physics = "Terre"
        self.mode = "Faire apparaitre une boîte"

        # Creation du sol
        floor_height = 100
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, floor_height], [LargeurEcran, floor_height], 0.0)
        shape.friction = 1.0
        shape.elasticity = 0.5
        self.space.add(shape)
        self.static_lines.append(shape)

    def on_draw(self):
        #Affichage de l'écran
        arcade.start_render()
        
        DrawStartTime = timeit.default_timer()
        
        arcade.draw_texture_rectangle(LargeurEcran // 2, HauteurEcran // 2,
                                      LargeurEcran, HauteurEcran, self.background)

        self.sprite_list.draw() #Affichage des sprites

        self.draw_time = timeit.default_timer() - DrawStartTime

        # Affichage des consignes d'utilisation à l'écran
        output = f"Mode: {self.mode}"
        arcade.draw_text(output, 20, HauteurEcran - 20, arcade.color.WHITE)

        output = f"Localisation: {self.physics}"
        arcade.draw_text(output, 20, HauteurEcran - 40, arcade.color.WHITE)
        
        output = f"Touches utiles :"
        arcade.draw_text(output, 1770, HauteurEcran - 20, arcade.color.WHITE)
        
        output = f"ESPACE - Déplacer les objets"
        arcade.draw_text(output, 1688, HauteurEcran - 40, arcade.color.WHITE)
        
        output = f"Clic gauche - Faire apparaitre un objet"
        arcade.draw_text(output, 1631, HauteurEcran - 60, arcade.color.WHITE)
        
        output = f"B - Faire apparaitre une boîte"
        arcade.draw_text(output, 1684, HauteurEcran - 80, arcade.color.WHITE)
        
        output = f"H - Faire apparaitre un homme"
        arcade.draw_text(output, 1673, HauteurEcran - 100, arcade.color.WHITE)
        
        output = f"V - Faire apparaitre une voiture"
        arcade.draw_text(output, 1670, HauteurEcran - 120, arcade.color.WHITE)
        
        output = f"E - Faire apparaitre un éléphant"
        arcade.draw_text(output, 1669, HauteurEcran - 140, arcade.color.WHITE)
        
        output = f"S - Aller dans l'espace"
        arcade.draw_text(output, 1730, HauteurEcran - 160, arcade.color.WHITE)
        
        output = f"L - Aller sur la Lune"
        arcade.draw_text(output, 1745, HauteurEcran - 180, arcade.color.WHITE)
        
        output = f"M - Aller sur Mars"
        arcade.draw_text(output, 1751, HauteurEcran - 200, arcade.color.WHITE)
        
        output = f"T - Revenir sur Terre"
        arcade.draw_text(output, 1736, HauteurEcran - 220, arcade.color.WHITE)
        
        output = f"Pour faire disparaître les objets :"
        arcade.draw_text(output, 20, HauteurEcran - 80, arcade.color.WHITE)
        
        output = f"Les déplacer hors de l'écran"
        arcade.draw_text(output, 20, HauteurEcran - 100, arcade.color.WHITE)

    # Définition des différents objets

    def SpawnBoîtes(self, x, y):
        taille = 50
        masse = 30
        moment = pymunk.moment_for_box(masse, (taille, taille))
        Objet = pymunk.Body(masse, moment)
        Objet.position = pymunk.Vec2d(x, y)
        Forme = pymunk.Poly.create_box(Objet, (taille, taille))
        Forme.elasticity = 0.5
        Forme.friction = 1.0
        self.space.add(Objet, Forme)
    
        sprite = Formes(Forme, "images/Boîte.png", width=taille, height=taille)
        self.sprite_list.append(sprite)
        
    def SpawnHumain(self, x, y):
        hauteur = 200
        largeur=100
        masse = 100
        moment = pymunk.moment_for_box(masse, (hauteur, largeur))
        Objet = pymunk.Body(masse, moment)
        Objet.position = pymunk.Vec2d(x, y)
        Forme = pymunk.Poly.create_box(Objet, (hauteur, largeur))
        Forme.elasticity = 0.4
        Forme.friction = 1.0
        self.space.add(Objet, Forme)
    
        sprite = Formes(Forme, "images/Homme.png", width=largeur, height=hauteur)
        self.sprite_list.append(sprite)
        
    def SpawnCar(self, x, y):
        hauteur = 100
        largeur=250
        masse = 1000
        moment = pymunk.moment_for_box(masse, (hauteur, largeur))
        Objet = pymunk.Body(masse, moment)
        Objet.position = pymunk.Vec2d(x, y)
        Forme = pymunk.Poly.create_box(Objet, (hauteur, largeur))
        Forme.elasticity = 0.3
        Forme.friction = 1.0
        self.space.add(Objet, Forme)
    
        sprite = Formes(Forme, "images/Voiture.png", width=largeur, height=hauteur)
        self.sprite_list.append(sprite)
        
    def SpawnElephant(self, x, y):
        hauteur=200
        largeur=400
        masse=5000
        moment = pymunk.moment_for_box(masse, (hauteur, largeur))
        Objet = pymunk.Body(masse, moment)
        Objet.position = pymunk.Vec2d(x, y)
        Forme = pymunk.Poly.create_box(Objet, (hauteur, largeur))
        Forme.elasticity = 0.3
        Forme.friction = 1.0
        self.space.add(Objet, Forme)
        
        sprite = Formes(Forme, "images/Elephant.png", width=largeur, height=hauteur)
        self.sprite_list.append(sprite)


    def get_shape(self, x, y):
        # Détecte le clic
        shape_list = self.space.point_query((x, y), 1, pymunk.ShapeFilter())

        # Garde en mémoire l'endroit du clic
        if len(shape_list) > 0:
            shape = shape_list[0]
            
        else:
            shape = None

        return shape

    # Lorsqu'on appuie sur la souris
    def on_mouse_press(self, x, y, button, modifiers):

        if button == 1 and self.mode == "Déplacer les objets":
            self.last_mouse_position = x, y
            self.shape_being_dragged = self.get_shape(x, y)

        elif button == 1 and self.mode == "Faire apparaitre une boîte":
            self.SpawnBoîtes(x, y)

        elif button == 1 and self.mode == "Faire apparaitre un humain":
            self.SpawnHumain(x, y)

        elif button == 1 and self.mode == "Faire apparaitre une voiture":
            self.SpawnCar(x, y)
            
        elif button == 1 and self.mode == "Faire apparaitre un éléphant":
            self.SpawnElephant(x, y)

    # Lorsqu'on relache le bouton
    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            # Lorsqu'on relache le clic, l'objet tombe
            self.shape_being_dragged = None
            
    # Durant le déplacement du curseur
    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            # Si on tient l'objet, il bouge avec le curseur
            self.last_mouse_position = x, y
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    # Lorsqu'on appuie sur un bouton du clavier
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.mode = "Déplacer les objets"
            
        elif symbol == arcade.key.B:
            self.mode = "Faire apparaitre une boîte"
            
        elif symbol == arcade.key.H:
            self.mode = "Faire apparaitre un humain"
            
        elif symbol == arcade.key.V:
            self.mode = "Faire apparaitre une voiture"
            
        elif symbol == arcade.key.E:
            self.mode = "Faire apparaitre un éléphant"

        elif symbol == arcade.key.S:
            self.space.gravity = (0.0, 0.0)
            self.space.damping = 1
            self.physics = "Espace"
            self.background = arcade.load_texture("images/Espace.png")
            
        elif symbol == arcade.key.T:
            self.space.damping = 1
            self.space.gravity = (0.0, -900.0)
            self.physics = "Terre"
            self.background = arcade.load_texture("images/Terre.jpg")
            
        elif symbol == arcade.key.M:
            self.space.damping = 0.9
            self.space.gravity = (0.0, -340.0)
            self.physics = "Mars"
            self.background = arcade.load_texture("images/Mars.jpg")
            
        elif symbol == arcade.key.L:
            self.space.damping = 0.9
            self.space.gravity = (0.0, -148.0)
            self.physics = "Lune"
            self.background = arcade.load_texture("images/Lune.jpg")

    def update(self, delta_time):
        start_time = timeit.default_timer()

        # Pour les objets qui sortent de l'écran
        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.position.y < 0:
                # On les supprimes de l'espace physique et de la liste physique
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                sprite.kill()

        # Mise à jour 
        self.space.step(1 / 80.0)

        # Pour être sur que l'objet suive le curseur et que la gravité agisse sur cet objet
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        # Mise à jour : les images doivent suivre la position de l'objet physique 
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        # Enregistrement du temps mis pour faire les actions, pour les afficher
        self.processing_time = timeit.default_timer() - start_time

window = Simulation(LargeurEcran, HauteurEcran, Titre)

arcade.run()