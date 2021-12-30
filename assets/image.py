db = {'3':['''Forward Sunshield Pallet

The Forward Unitized Pallet Structure (UPS).

This step begins the Sunshield deployment phase.

Nominal Event Time: Launch + 3 days

The UPS supports and carries the five folded sunshield membranes. Prior to this, the spacecraft is maneuvered to provide warmer temperatures on the forward UPS and various heaters are activitated to warm key deployment components. Key release devices are activated. Various electronics and software are configured prior to support the UPS motions, which are driven by a motor. This step represents the start of the Sunshield deployment phase and the start of all major deployments.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/107.png'],
'3.5': ['''Aft Sunshield Pallet

The Aft Unitized Pallet Structure (UPS)

Nominal Event Time: Launch + 3 days

The UPS supports and carries the five folded sunshield membranes. Prior to this, the spacecraft will have been maneuvered to provide warmer temperatures on the forward UPS and various heaters have been activitated to warm key deployment components. Key release devices have been activated. Various electronics and software have also been configured prior to support the UPS motions, which are driven by a motor.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/108.png'],
'4':['''DTA Deployment
Deployable Tower Assembly (DTA)

Nominal Event Time: Launch + 4 days

The Deployable Tower Assembly (DTA) is deployed. The tower will extend about 2 meters. This movement/distance provides needed separation between the spacecraft and telescope to allow for better thermal isolation and to allow room for the sunshield membranes to unfold. Prior to this, several release devices will have been activated, and various heaters, software, and electronics have been configured to support deployments. This deployment motion is driven by a motor.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/109.png'],
'5':['''Aft Momentum Flap
Nominal Event Time: Launch + 5 days

The Aft Momentum Flap is used to help offset some of the solar pressure that impinges on the large sunshield. Use of the momentum flap helps to minimize fuel usage during the mission. After releasing hold-down devices, a spring drives the rotation of the aft flap to its final position.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/110.png'],
'5.5':['''Sunshield Covers Release
Nominal Event Time: Launch + 5 days

This operation releases and rolls up the protective membrane cover. The sunshield release cover has been protecting the membranes during ground and launch activities. Release devices are electrically activated to release the covers.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/111.png'],
'6':['''Sunshield PORT Mid-Boom
The Left/Port (+J2) Sunshield Boom Deployment

Nominal Event Time: Launch + 6 days

The Port +J2 Mid-boom deployment steps include the completion of the sunshield cover roll up, the deployments team then extends the +J2 mid-boom along with the +J2 side of the five membranes. This operation is a motor-driven deployment.''','https://www.jwst.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/112.png']

}
from time import strftime,gmtime
def get_image():
    global db
    d = str(int(strftime('%d',gmtime())) - 25)
    if d in (3,5):
        h = strftime('%H',gmtime())
        if int(h) > 12:
            return db[d+'.5']
        return db[h]
    else:
        return db[d]
    


