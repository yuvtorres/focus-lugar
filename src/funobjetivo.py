import numpy as np
import research_tool
# Función Objetivo

# recibe un array de puntos (Lat, Lng) y retorna el valor de la función

def fun_objetivo(x):
    point=(x[0],x[1])

    Val_by_place={"other Design companies":research_tool.val_design(point),
         "kindergarden":research_tool.val_kindergarden(point),
         "success startup":research_tool.val_succ(point),
         "Starbucks":research_tool.val_starbucks(point),
         "Airport_or_train_station":research_tool.val_airport(point),
         "place_to party":research_tool.val_party(point),
         "basqueball court":research_tool.val_basquet(point),
         "no_2km_old_company":research_tool.val_old(point),
         "vegan_restaurant":research_tool.val_vegetariano(point)}

    return valor(**Val_by_place)


# función de valoración
# recibe como argumento el siguiente diccionario:
#    Val_by_place={"other Design companies":0,
#         "kindergarden":0,
#         "success startup":0,
#         "Starbucks":0,
#         "Airport_or_train_station":0,
#         "place_to party":0,
#         "basqueball court":0,
#         "no_2km_old_company":0,
#         "vegan_restaurant":0}


def valor(**Val_by_place):
# Constants:
# Total personal (9 x 1)
    Personal={"Designers":20,
         "UI/UX Engineers":5,
         "Frontend Developers":10,
         "Data Engineers":15,
         "Backend Developers":15,
         "Account Managers":20,
         "Maintenance guy":1,
         "Executives":10,
         "CEO/President":1}

# Valoration of the contribution to grow by role (9 x 1)
    Val_to_grow={"Designers":5,
         "UI/UX Engineers":5,
         "Frontend Developers":5,
         "Data Engineers":5,
         "Backend Developers":5,
         "Account Managers":7,
         "Maintenance guy":3,
         "Executives":8,
         "CEO/President":10}

# Rel_personal_Val_place represent the relation between condition and personal (9 x 9)

    Rel_personal_Val_place =[
    [1,0,0,0,0,0,0,0,0], # other Design companies -> Designers
    [0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3], # kindergarden -> 30% of the personal
    [0,1,1,1,1,0,0,0,0], # success startup
    [0,0,0,0,0,0,0,1,0], # Starbucks
    [0,0,0,0,0,1,0,0,0], # airport..
    [1,1,1,1,1,1,1,1,1], # place to party
    [0,0,0,0,0,0,1,0,0], # Basquetball court
    [1,1,1,1,1,1,1,1,1], # No old company (10 years)
    [0,0,0,0,0,0,0,0,1], # vegan restauran
]

    # Any places will be valuated with the next equation:
    #               constant                                 Independient Variable
    # F = (Personal * Val_to_grow * Rel_personal_Val_place)  *    Val_by_place

    val=np.array(list(Val_by_place.values()))
    pers=np.array(list(Personal.values()))
    vgrow=np.array(list(Val_to_grow.values()))
    Per_Val=np.array((Rel_personal_Val_place))
    temp1=np.matmul(Per_Val,val)
    temp2=np.matmul(pers,np.diag(vgrow))
    return np.matmul(temp1,temp2)
