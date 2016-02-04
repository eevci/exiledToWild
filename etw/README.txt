Exiled To Wild
*Enver Evci 1942085	
*Onat Büyükakkuş 2035772

***mysql library'sini kullanarak database'e bağlanmak için, bağlanma bilgilerini etwClasses.py dosyasında global olarak tanımladığımız değişkenleri kullanarak değiştirebilirsiniz.

***etw.py dosyasını çalıştırdığınızda, New Game ve Continue olarak 2 seçenekle karşılacaksınız, New Game tüm gridi baştan yaratıp, database'e kaydediyor, bu sebeple 10 dakikaya yakın bir süre tutuyor. Ancak kullanıcı tarafından değil, server tarafından bir kere uygulanacak bir komut, sql tablolarımız sizde olmadığı için böyle bir yöntem kullandık. Harita bir kere yaratıldıktan sonra Continue seçeneğine tıklarsanız, New User ya da Existing User seçeneklerini kullanarak var olan haritaya yeni ya da önceden oluşturulmuş kullanıcı ekleyerek oynayabilirsiniz. Continue seçeneği oyuncuların kullandığı seçenek olacak, oyuncular haritayı yeniden yaratma seçeneğine sahip olamayacak (New Game).

***Komutlar:
	move -> direction yönünde bir birim hareket eder.
	turn Up/Down/Left/Right -> kullanıcının yönünü değiştirir.
	take -> direction yönündeki bir birim uzaklıktaki silahı inventory'e ekler.
	select Sword/Axe/Dagger/Punch -> inventory'de bulunan silahlardan birini ya da default silah olan punch'ı seçer.
	attack -> direction yönündeki bir birim uzaklıktaki hayvana saldırır.
	cut -> direction yönündeki bir birim uzaklıktaki ağacı keser.
	
