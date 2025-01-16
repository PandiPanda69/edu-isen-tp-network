# TP1 - Virtualisation : Proxmox, Linux & Networking

_Sébastien Mériot_ ([@smeriot](https://twitter.com/smeriot))

Durée: 3 heures

Introduction
=====================

Dans les architectures modernes, la virtualisation occupe une place prépondérante afin de pouvoir
utiliser au mieux la puissance des machines (comprendre, maximiser l'utilisation du CPU et de la
RAM afin de rationnaliser les coûts de consommation).

La virtualisation apporte également un avantage de flexibilité considérable puisqu'il est possible
de créer et de supprimer des machines virtuelles facilement. Fonctionnalité souvent méconnue, les
hyperviseurs permettent également d'assurer des niveaux de service (SLA) en offrant la possibilité
de migrer les machines virtuelles à chaud, de façon transparente d'une machine hôte à une autre.

Dans ce TP, nous allons nous familiariser avec [KVM](https://fr.wikipedia.org/wiki/Kernel-based_Virtual_Machine) au travers de [Proxmox](https://www.proxmox.com/), des solutions opensource très utilisées. Notamment KVM est la solution de choix pour les différents fournisseurs de Cloud Public (AWS, OVHcloud, Digital Ocean, ...).

Disclaimer
=====================

Dans ce TP, vous allez partager une même instance Proxmox pour les différents groupes de TP. Cela vous permettra de voir qu'il est possible de travailler simultanément sur un même hôte physique.

Première connexion
=====================

A l'aide des identifiants communiqués en cours, connectez-vous sur l'interface de gestion de Proxmox.

L'interface se décompose en 3 parties :
- A gauche, vous avez la vue générale des serveurs hôtes et des machines virtuelles qui tournent.
- Le panneau centrale affiche les informations détaillées des éléments selectionnés au travers du panneau de gauche.
- En bas, vous avez les différents *logs*. Chaque action générera des traces avec des status d'avancement. Etant donné que vous partagez la même instance à plusieurs, vous verrez également les actions des autres équipes.

Sur le panneau de gauche, il est possible de changer la visualisation. Celle par défaut est assez naïve avec un arbre représentant un *Datacenter* composé des hôtes portant chacun des machines virtuelles. Vous pouvez changer la visualisation à l'aide de la liste déroulante juste au dessus en sélectionnant par exemple la *Folder View* qui présente les différentes éléments du *Datacenter* sous une forme plus pertinent (c'est un avis personnel bien évidemment).

Quelque soit la vue, vous devriez voir apparaître le seul et unique hôte de notre cluser nommé `proxmox1`. Cliquez sur cet élément. En cliquant sur l'onglet `Summary` du panneau central, vous verrez l'état de la machine hôte qui va venir accueillir vos différentes machines virtuelles.

1. Indiquez le nombre de coeurs et la quantité de RAM disponible.
2. Selon vous, en considérant des petits VM ayant 1 vCPU et 2 GB de RAM, combien de VM au plus est-il possible de faire tourner simultanément sur cet hôte ?


Création des utilisations
=====================

Une bonne pratique d'administration et de sécurité consiste à toujours utiliser des comptes utilisateur nominatifs. Cela permet notamment de mieux tracer les actions de chacun (auditabilité).

3. Pour créer des utilisateurs, il faut commencer par créer un groupe. En cliquant sur le *Datacenter*, puis sur l'onglet `Groups` du panneau central sous la rubrique `Permissions`, créer un nouveau groupe ayant pour nom `Groupe_X` où `X` est le numéro qui vous sera affecté par votre encadrant.

4. Vous pouvez à présent créer autant d'utilisateur que de personnes dans votre groupe dans cliquant sur l'onglet `Users`. Saisissez un nom d'utilisateur, un mot de passe et sélectionnez la méthode d'authentification PVE (Authentification Proxmox, à contratio de l'authentification [PAM](https://en.wikipedia.org/wiki/Pluggable_Authentication_Module)). Affectez à chaque utilisateur le nouveau nouvellement créé.

5. Les nouveaux comptes créés peuvent être directement utilisés. Néanmoins, vous devriez vous rendre compte en vous connectant que l'interface est bien vide... En effet, aucun privilége n'est donné par défaut aux nouveaux comptes/groupes. Allez à présent dans l'onglet `Permissions`, et ajoutez une nouvelle permission. Etant donné les besoins du TP, nous allons uniquement donné des droits de manipulation des VM pour le moment. Cliquez sur `Add`, puis `Group permissions`. Saississez le *Path* tel que `/`, sélectionnez votre groupe, puis le rôle `PVEVMAdmin` ce qui vous donnera les privilèges de gestion intégrale des VM. Raffraichissez l'interface pour les utilisateurs connectés et constatez que vous avez des options supplémentaires à présent !

Création de votre première VM
=====================

## Download an image

## Configuration

## Start

## Install the OS

## Play

Network configuration
=====================

## Bridge

## NAT

Communication between 2 VMs
=====================

Communication with the Internet
=====================

Cisco iOS XE
=====================
