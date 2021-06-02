class GameRole:
    def __init__(self, name, ad, hp):
        self.name = name
        self.ad = ad
        self.hp = hp

    def attack(self, p):
        p.hp = p.hp - self.ad
        if p.hp > 0:
            print("%s攻击%s，%s掉了%s点血，还剩%s点血"
                  % (self.name, p.name, p.name, self.ad, p.hp))
        else:
            print(p.name + "死亡")

    def arm_weapon(self, wea):
        self.wea = wea


class Weapon:
    def __init__(self, name, ad):
        self.name = name
        self.ad = ad

    def fight(self, p1, p2):
        p2.hp = p2.hp - self.ad
        if p2.hp > 0 and p1.hp > 0:
            print("%s用%s打了%s,%s掉了%s点血，还剩下%s点血"
                  % (p1.name, self.name, p2.name, p2.name, self.ad, p2.hp))
        else:
            p2.hp = 0
            # print(p2.name + "死亡,游戏结束")


p1 = GameRole("盖伦", 20, 500)
p2 = GameRole("亚索", 50, 400)
axe = Weapon("斧头", 60)
sward = Weapon("屠龙宝刀", 100)

p1.arm_weapon(axe)
p2.arm_weapon(sward)

count = 0
while 1:  # 你们开始打吧，哈哈，管我毛事
    print("第%s回合" % (count + 1))

    if p1.hp > 0:
        p1.wea.fight(p1, p2)

    if p2.hp > 0:
        p2.wea.fight(p2, p1)

    if p1.hp <= 0:
        print("%s用%s把%s打死了，%s获胜，游戏结束，让我们恭喜%s！"
              % (p2.name, p2.wea.name, p1.name, p2.name, p2.name))
        break

    if p2.hp <= 0:
        print("%s用%s把%s打死了，%s获胜，游戏结束，让我们恭喜%s！"
              % (p1.name, p1.wea.name, p2.name, p1.name, p1.name))
        break

    count += 1
