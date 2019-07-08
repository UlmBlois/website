# Chunk Detail

## Global Message

Template : includes/alert_messages.html

|chunk                |evaluation|
|---------------------|----------|
|global_info_messsage |   safe   |

## Page index

Template : meeting/index.html

|chunk                 |evaluation|
|----------------------|----------|
|ulm_pilot_short       |   safe   |
|ppl_pilot_short       |   safe   |
|paramotor_pilot_short |   safe   |
|exhibitor_short       |   safe   |
|presentation_short    |   safe   |
|presentation_short_2  |   safe   |

## Page about

Template : pages/about.html

|   chunk   | evaluation |
|-----------|------------|
|about_page | eval       |

## Page contact

Template : pages/contact.html

| chunk       | evaluation |
|-------------|------------|
|contact_page | safe       |

## Page pilot information

Template : pages/pilot_informations.html


| chunk                | evaluation |
|----------------------|------------|
| pilot_info_general   |    safe    |
| pilot_info_arrival   |    safe    |
| pilot_info_departure |    safe    |
| pilot_info_paramotor |    safe    |
| pilot_info_plane     |    safe    |


## Page on site

Template : pages/on_site.html

| chunk        | evaluation  |
|--------------|-------------|
| on_site_pape | safe        |


## Page logged index

Template : meeting/logged_index.html

| chunk                    | evaluation |
|--------------------------|------------|
| registration_procedure_1 | safe       |
| registration_procedure_2 | safe       |
| registration_procedure_3 | safe       |


## Page Terms and Conditions

Template : pages/terms.html

| chunk     | evaluation |
|-----------|------------|
|terms_page |   safe     |


## Page Copyright

Template : pages/copyright.html

| chunk         | evaluation |
|---------------|------------|
|copyright_page |   safe     |


## Page Privacy

Template : pages/privacy.html

| chunk       | evaluation |
|-------------|------------|
|privacy_page |   safe     |


## Email Reservation confirmation request

Template : emails/reservation_confirmation_request.html

| chunk                   | evaluation |
|-------------------------|------------|
| email_res_confirm_body_1 | safe       |
| email_res_confirm_body_2 | safe       |


## Email Password reset

Template : emails/password_reset_email.html

| chunk                   | evaluation | Variables |
|-------------------------|------------|-----------|
| email_password_reset    | render     | email, protocol, domain, uid, token|

/!\ Ne pas modifier les variables

# Importer et Exporter

Il est possible d'importer et d'exporter la liste des pages et des bloc.

## Précautions

L'import de donné dans une base déjà remplis peu avoir des effet indésiré:
* modification non voulu (clef privée différentes entre le fichier et la base)
* duplication d'entrée (clef privée différentes entre le fichier et la base)

Il est conseillé de faire un back up ou un export de la base avant tout import.
Dans le cas ou l'import aurais causé des problème d'intégrité des données, supprimer
toutes les entrées et repartez de vos backup ou du fichier a importer si il reprend toute la base.
Sinon faites corrigez le fichier a importer afin qu'il corresponde a la base dans laquelle il sera intégré.
 
