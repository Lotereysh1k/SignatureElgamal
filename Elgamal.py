import math
import random
import gmpy2

# Спизженно и переписано на коленке, чтобы могло считать p > 512 бит
# Если есть желание провести рефакторинг - флаг вам в руки
# Если есть пожелания, критика(мне похуй) можете писать на почту zxcwert@fbi.ac
# Спонсор данного кода - 15 баллов по крипте(могло быть 20).

class signAlgo :

    def __init__(self,a,b,c,d):
        self.p=gmpy2.mpz(a)  # простое число p
        self.alpha=gmpy2.mpz(b) # параметр открытого ключа g
        self.beta=gmpy2.powmod(self.alpha,z,self.p) # вычисляем открытый ключ
        self.m=c # сообщение m
        self.k=d # Случайное число k <-- хуета по приколу, смысла не имеет
        self.inv_k=self.NewInvK() #обратное к k
        self.r=self.createR() # Подпись R
        self.s=self.createS() # Подпись S
        print ("Сгенерированная тройка сообщений(openkey,r,s) : ("+str(self.beta)+","+str(self.r)+","+str(self.s)+")")
    
    def gcd(self, a, b ): # Вычисление НОД
        while b != 0:
            c = a % b
            a = b
            b = c
        return a

    def NewInvK(self): # <-- Обратное значение k
        inv_k=None
        while inv_k is None:
            try:
                inv_k = pow(self.k, -1, self.p-1)
            except ValueError:
                self.k = random.randint(2, self.p-2)
        print(f'Найденный обратный элемент взаимнопростой с p: {inv_k}')
        return inv_k
    
    def createR(self):  # Вычисляем R
        a=gmpy2.powmod(self.alpha,self.k,self.p) 
        return a
    
    def createS(self): # Вычисляем S
        a=(self.inv_k*(self.m-z*self.r))%(self.p-1)
        return a

class verify:	# Проверка подлинности подписи
	def __init__(self,a,b,c,d,e,f):
		self.p=a # простое число p
		self.alpha=b # параметр  g
		self.beta=gmpy2.mpz(c) # открытый ключ
		self.m=d # сообщение m
		self.r=e # Подпись R
		self.s=f # Подпись S
	def v1(self,b,c,d,a): # 
		a = gmpy2.powmod(gmpy2.mul(gmpy2.powmod(gmpy2.mpz(b), gmpy2.mpz(c), gmpy2.mpz(self.p)), gmpy2.powmod(gmpy2.mpz(c), gmpy2.mpz(d), gmpy2.mpz(self.p))), 1, gmpy2.mpz(self.p))
		return a

	def v2(self,b,c):
		a = gmpy2.powmod(gmpy2.mpz(b), gmpy2.mpz(c), gmpy2.mpz(self.p))
		return a

	def verified(self):
		if(self.v1(self.beta,self.r,self.s,self.p)==self.v2(self.alpha,self.m)):
			print("Правильная подпись")
			print("Проверка v1: "+str(self.v1(self.beta,self.r,self.s,self.p)))
			print("Проверка v2: "+str(self.v2(self.alpha,self.m)))
		else:
			print("Неправильная подпись")
			print("Проверка v1: "+str(self.v1(self.beta,self.r,self.s)))
			print("Проверка v2: "+str(self.v2(self.alpha,self.m)))

def gcd(a, b ): # Вычисление НОД. Да, я в курсе, что это есть в классе, но мне похуй.
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def generate_coprime(p): #Случайное k взаимнопростое с p
    while True:
        k = random.randint(2, p-1)
        if gcd(k, p) == 1:
            return k

def modexp( base, exp, modulus ):
		return pow(base, exp, modulus)

def find_primitive_root( p ):
		if p == 2:
				return 1

		p1 = 2
		p2 = (p-1) // p1

		while( 1 ):
				g = random.randint( 2, p-1 )
				if not (modexp( g, (p-1)//p1, p ) == 1):
						if not modexp( g, (p-1)//p2, p ) == 1:
								return g

# Генератор простых больших чисел
        # |
        # | 
def is_prime(n, k=5):
    """Проверяет, является ли число n простым с вероятностью ошибки 1/4^k."""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Представляем n-1 как (2^r) * d, где d нечётное
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Повторяем тест Миллера-Рабина k раз
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_bit_prime(z): # Генерирует простое n битное число
    while True:
        number = random.getrandbits(z) | (1 << z-1) | 1  # Установка старшего и младшего битов в 1
        if is_prime(number):
            return number

p=generate_bit_prime(2048)
g=(find_primitive_root(p)) # <-- первообразный(g) от p
m=int(input("Введите сообщение m: "))
k=generate_coprime(p) # <-- чисто по приколу, чтобы самому переменную не объявлять
print(f'Значение k: {k}') # <-- Посмотреть, что сгенерировала хуета выше
z=int(input('Секретный ключ x: ')) 
sign=signAlgo(p,g,m,k)

print ("Проверка подписи Эль-Гамаля")
v=verify(sign.p,sign.alpha,sign.beta,sign.m,sign.r,sign.s)
v.verified()
