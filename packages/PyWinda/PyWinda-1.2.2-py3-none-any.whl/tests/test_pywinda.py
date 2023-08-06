from PyWinda import pywinda
def test_haversine():
    assert pywinda.haversine(52.370216, 4.895168, 52.520008, 13.404954) == 945793.4375088713

    farm=pywinda.environment("Curslack")
    assert farm.test()=="Curslack"