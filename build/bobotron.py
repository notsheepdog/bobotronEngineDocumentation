# python3.10 bobotron.py -m ./bobotronEngine.so

import bobotronEngine

# Initialize SDL
screenH = 400;
screenW = 400;
SDLProg = bobotronEngine.SDLGraphicsProgram(screenW,screenH)

pauseGame = False;

# Set up Player
player = SDLProg.CreateGameEntity("Assets/SolarHero.bmp");

# Set up Enemies
enemies = [];

# Set up Friendlies
friendlies = [];

# Set up bullets (represented by their chase components)
bullets = [];

# Set up Scene Levels
sceneIdx = 0;
scenes = []
scenes.append("Scenes/StartScreen.txt");
scenes.append("Scenes/Level1.txt");
scenes.append("Scenes/Level2.txt");
scenes.append("Scenes/Level3.txt");
scenes.append("Scenes/Level4.txt");
scenes.append("Scenes/Victory.txt");

# Set up Scene Loading
def LoadScene(filePath):
    global pauseGame

    file = open(filePath,'r');
    content = file.readlines()

    enemies.clear();
    friendlies.clear();
    bullets.clear();

    i = 0
    while i < len(content):
        # Set up paused game screen (start / game over / victory)
        if content[i].startswith("pause"):
            entityInfo = content[i].split();
            entity = SDLProg.CreateGameEntity(entityInfo[1]);
            entityTrans = bobotronEngine.TransformComponent();
            entityTrans.SetWH(400, 400);
            entity.AddComponent(entityTrans);
            enemies.append(entity);
            pauseGame = True;
        # Set up player
        if content[i].startswith("player"):
            entityInfo = content[i].split();
            player.Move(-1 * screenW, -1 * screenH); # non-elegant solution, fine for this scope
            player.Move(int(entityInfo[1]), int(entityInfo[2]));
        # set up enemies
        elif content[i].startswith("grunt"):
            assetPath = "Assets/BobotGrunt.bmp";

            entityInfo = content[i].split(); # enemy info is [name] [xDir] [yDir] [xCoord] [yCoord]

            # dynamically choose sprite based on enemy's movement capabilities
            if int(entityInfo[1]) < 1:
                assetPath = "Assets/BobotUpStepper.bmp"
            elif int(entityInfo[2]) < 1:
                assetPath = "Assets/BobotSideStepper.bmp"
            bobotGrunt = SDLProg.CreateGameEntity(assetPath);
            
            bobotGrunt.Move(int(entityInfo[3]), int(entityInfo[4]));
            gruntChase = bobotronEngine.ChaseComponent();
            gruntChase.CreateChaseComponent(bobotGrunt, player, int(entityInfo[1]), int(entityInfo[2]));
            bobotGrunt.AddComponent(gruntChase);
            enemies.append(bobotGrunt);
        # set up friendlies
        elif content[i].startswith("sitfriendly"):
            friendly = SDLProg.CreateGameEntity("Assets/SittingFriendly.bmp");
            entityInfo = content[i].split();
            friendly.Move(int(entityInfo[1]), int(entityInfo[2]));
            friendlies.append(friendly);
        elif content[i].startswith("standfriendly"):
            friendly = SDLProg.CreateGameEntity("Assets/StandingFriendly.bmp");
            entityInfo = content[i].split();
            friendly.Move(int(entityInfo[1]), int(entityInfo[2]));
            friendlyWander = bobotronEngine.WanderComponent();
            friendlyWander.CreateWanderComponent(friendly, 2);
            friendly.AddComponent(friendlyWander);
            friendlies.append(friendly);
        i = i + 1;
    file.close();

# Load first scene
LoadScene(scenes[sceneIdx]);

shootingCooldownMax = 30;
shootingCooldown = 0;

# Our main game loop
print("Setting up game loop")
while not SDLProg.QuitGame():
    # Clear the screen
    SDLProg.clear();

    # PLAYER
    if pauseGame:
        if SDLProg.AKeyPressed() and SDLProg.DKeyPressed():
            pauseGame = False;
            sceneIdx = 1;
            LoadScene(scenes[sceneIdx]);
    else:
        # movement
        xMovement = SDLProg.DKeyPressed() * 3 + SDLProg.AKeyPressed() * -3;
        yMovement = SDLProg.SKeyPressed() * 3 + SDLProg.WKeyPressed() * -3;
        player.Move(xMovement, yMovement);
        SDLProg.RenderGameEntity(player);

        # shooting
        if (shootingCooldown <= 0) :
            xShoot = SDLProg.RightKeyPressed() * 5 + SDLProg.LeftKeyPressed() * -5;
            yShoot = SDLProg.DownKeyPressed() * 5 + SDLProg.UpKeyPressed() * -5;
            if xShoot != 0 or yShoot != 0:
                heroBullet = SDLProg.CreateGameEntity("Assets/SolarBullet.bmp");
                heroBullet.Move(player.GetTransform().GetX(), player.GetTransform().GetY());
                heroBulletLaunch = bobotronEngine.LaunchComponent();
                heroBulletLaunch.CreateLaunchComponent(heroBullet, xShoot, yShoot);
                heroBullet.AddComponent(heroBulletLaunch);
                bullets.append(heroBulletLaunch);
                shootingCooldown = shootingCooldownMax;
        else :
            shootingCooldown = shootingCooldown - 1;
    
    # FRIENDLIES
    remainingFriendlies = [];
    for f in friendlies:
        f.Update();
        SDLProg.RenderGameEntity(f);
        if not player.Intersects(f):
            remainingFriendlies.append(f);
    friendlies = remainingFriendlies;

    if len(friendlies) == 0 and not pauseGame:
        sceneIdx = sceneIdx + 1;
        LoadScene(scenes[sceneIdx]);
    

    # ENEMIES
    remainingEnemies = [];
    enemyKillsPlayer = False;
    for e in enemies:
        e.Update();
        SDLProg.RenderGameEntity(e);

        # has the enemy hit the player?
        if player.Intersects(e) and not pauseGame:
            enemyKillsPlayer = True;            

        # logic for if enemy is killed by bullet
        # not totally optimal, but it works fine for this scope
        keepEnemy = True;
        for b in bullets:
            if b.GetGameEntity().Intersects(e):
                keepEnemy = False;
                break;
        if keepEnemy:
            remainingEnemies.append(e);
    enemies = remainingEnemies;
    if enemyKillsPlayer:
        LoadScene('Scenes/GameOver.txt');

    # BULLETS
    remainingBullets = [];
    for b in bullets:
        b.Update();
        SDLProg.RenderGameEntity(b.GetGameEntity());
        if not b.HittingEdge():
            remainingBullets.append(b);
        # if b.GetGameEntity().Intersects(bobotGrunt):
        #     bobotGrunt.Move(50);
    bullets = remainingBullets;

    # Add a little delay
    SDLProg.delay(10);
    # Refresh the screen
    SDLProg.flipBuffer();