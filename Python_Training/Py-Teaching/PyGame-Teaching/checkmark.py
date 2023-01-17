#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
import time

FPS = 60
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
display1 = pygame.display.set_mode((w , h))
pygame.display.set_caption("Test")
#pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

current_scene = None
clock = pygame.time.Clock()
running = True

def CreateEmtySurf(SizeWidth: int = 24, SizeHeight: int = 24):
	return pygame.Surface((SizeWidth, SizeHeight), pygame.SRCALPHA, 32).convert_alpha()

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

def SwitchScene(scene):
	global current_scene
	current_scene = scene

def RenderCheckMark(color = (0, 0, 0), size: int = 30, width: int = 5):
	font = pygame.font.Font(str(pathlib.Path('./SegoeUISymbol.ttf').resolve()), size)
	mark_surf = font.render('✓', 1, color)
	mark_surf_rect = mark_surf.get_rect(topleft = (0, 0))
	checkmark_surf = pygame.Surface((mark_surf_rect.width, mark_surf_rect.height + width), pygame.SRCALPHA, 32).convert_alpha()
	i = 0
	for j in range(width + 1):
		checkmark_surf.blit(mark_surf, (0, j))
	return checkmark_surf

def work():
	global display1, clock, running, w, h
	
	bg_color = (64, 64, 64)
	menu_color = (240, 240, 240)
	frame_color = (166, 166, 166)
	select_color = (48, 150, 250)
	
	display1.fill(bg_color)
	pygame.display.update()
	font = pygame.font.Font(str(pathlib.Path('./SegoeUISymbol.ttf').resolve()), 30)
	text = font.render('Text', 1, (0, 0, 0))
	
	checkmark = RenderCheckMark((0, 0, 0), 26, 5)
	display1.blit(checkmark, (100, 100))
	display1.blit(text, (120, 100))
	display1.blit(LoadSurf(pathlib.Path('./checkmark-round.png')), (200, 100))
	pygame.display.update()
		
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			#elif event.type == STOPPED_PLAYING:
				# pass
			elif event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_F2:
				#	pass
				pass
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pass
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				pass
		
		#keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	pass
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		clock.tick(FPS)

def main():
	SwitchScene(work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()
