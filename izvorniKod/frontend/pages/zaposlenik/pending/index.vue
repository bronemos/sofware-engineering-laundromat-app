<template>
  <div class="root">
      <div>
          <NuxtLink to="/">Home</NuxtLink>
          <!-- <NuxtLink to="/login">Login</NuxtLink> -->
          <NuxtLink to="/zaposlenik/pending">Zaposlenik</NuxtLink>
      </div>
      <table>
        <thead>
          <tr>
            <th>Ima Studenta</th>
            <th>Status</th>
            <th>Akcije</th>
          </tr>
        </thead>
        <tbody>
          <!-- za našu bazu promijeniti isActive u aktivan -->
          <tr v-for="i in pending" :key="i" v-bind:class="i.isActive ? 'hide_btn' : 'show_btn'">
            <td>{{i.name}}</td>
            <td>{{i.isActive ? 'Active' : 'Inactive'}}</td>
            <td><button id="myBtn"  @click="i.isActive=true">Activate</button></td>
          </tr>
        </tbody>
      </table>
   </div>
</template>

<!-- maknuti hardkodirani json u pending -->
<script>
export default {
    data() {
        return {
            pending: [
  {
    "_id": "5fa3fd7fdbd1a952da115f03",
    "index": 0,
    "guid": "aa38f336-2b06-42e3-bb56-768e7cd686e8",
    "isActive": false,
    "balance": "$1,101.87",
    "picture": "http://placehold.it/32x32",
    "age": 35,
    "eyeColor": "blue",
    "name": "Ina Ramsey",
    "gender": "female",
    "company": "ISOSURE",
    "email": "inaramsey@isosure.com",
    "phone": "+1 (816) 575-2481",
    "address": "375 Ruby Street, Gibsonia, Alabama, 3389",
    "about": "Proident ipsum magna nulla consectetur veniam eu ut. Mollit ex ipsum nisi minim sunt esse dolor proident nisi voluptate nisi enim sunt dolore. Tempor in anim officia tempor enim laboris cupidatat exercitation non cillum.\r\n",
    "registered": "2019-11-07T05:12:29 -01:00",
    "latitude": -49.414066,
    "longitude": 56.714943,
    "tags": [
      "magna",
      "ad",
      "et",
      "velit",
      "voluptate",
      "eu",
      "minim"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Lucile Mercado"
      },
      {
        "id": 1,
        "name": "Cristina Torres"
      },
      {
        "id": 2,
        "name": "Benton Ellison"
      }
    ],
    "greeting": "Hello, Ina Ramsey! You have 8 unread messages.",
    "favoriteFruit": "banana"
  },
  {
    "_id": "5fa3fd7fa4823f08616f5e07",
    "index": 1,
    "guid": "7c18e4ca-fc04-4103-b61d-caae6910254b",
    "isActive": false,
    "balance": "$1,551.37",
    "picture": "http://placehold.it/32x32",
    "age": 39,
    "eyeColor": "green",
    "name": "Tabatha Jackson",
    "gender": "female",
    "company": "PURIA",
    "email": "tabathajackson@puria.com",
    "phone": "+1 (801) 477-2835",
    "address": "955 Rose Street, Croom, Federated States Of Micronesia, 4684",
    "about": "Culpa duis consectetur veniam minim magna veniam fugiat id tempor proident quis. Lorem nulla Lorem mollit ipsum. Sunt cupidatat quis labore consequat ea minim exercitation laboris id. Est velit minim velit consequat do.\r\n",
    "registered": "2020-07-24T12:58:38 -02:00",
    "latitude": -67.560025,
    "longitude": -89.996862,
    "tags": [
      "velit",
      "labore",
      "eiusmod",
      "cillum",
      "in",
      "elit",
      "veniam"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Hester Mcbride"
      },
      {
        "id": 1,
        "name": "Greene Alvarado"
      },
      {
        "id": 2,
        "name": "Joanne Koch"
      }
    ],
    "greeting": "Hello, Tabatha Jackson! You have 10 unread messages.",
    "favoriteFruit": "apple"
  },
  {
    "_id": "5fa3fd7f68a6565c16f94589",
    "index": 2,
    "guid": "88d232e3-c16f-4fb1-82a6-d484515a3fae",
    "isActive": false,
    "balance": "$2,516.90",
    "picture": "http://placehold.it/32x32",
    "age": 34,
    "eyeColor": "blue",
    "name": "Page Giles",
    "gender": "male",
    "company": "TERRAGO",
    "email": "pagegiles@terrago.com",
    "phone": "+1 (955) 430-3773",
    "address": "926 Drew Street, Lumberton, New Mexico, 9324",
    "about": "Dolore aliqua reprehenderit fugiat do consequat aliquip deserunt. Consequat non quis aute quis aute ut sit officia cillum voluptate do. Dolore minim eu sint voluptate proident ullamco minim veniam minim. Ipsum excepteur Lorem veniam ut ipsum proident voluptate sint labore.\r\n",
    "registered": "2017-07-19T09:14:11 -02:00",
    "latitude": -82.73534,
    "longitude": 13.497283,
    "tags": [
      "officia",
      "nulla",
      "incididunt",
      "esse",
      "Lorem",
      "dolore",
      "sint"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Reba Richmond"
      },
      {
        "id": 1,
        "name": "Sarah James"
      },
      {
        "id": 2,
        "name": "Mae Pate"
      }
    ],
    "greeting": "Hello, Page Giles! You have 7 unread messages.",
    "favoriteFruit": "banana"
  },
  {
    "_id": "5fa3fd7fd2edc3ec2ec83506",
    "index": 3,
    "guid": "66d168e4-6e5d-426c-bcfa-72e7de624f35",
    "isActive": false,
    "balance": "$2,621.21",
    "picture": "http://placehold.it/32x32",
    "age": 40,
    "eyeColor": "green",
    "name": "Olive Hopper",
    "gender": "female",
    "company": "GEEKKO",
    "email": "olivehopper@geekko.com",
    "phone": "+1 (844) 492-3943",
    "address": "151 Richmond Street, Greenock, Montana, 1124",
    "about": "Sunt elit culpa Lorem sunt tempor cupidatat aute velit cillum. Pariatur id cillum nulla consequat irure enim culpa est deserunt occaecat. Occaecat sit labore exercitation non pariatur labore amet irure magna laboris mollit. Culpa ex Lorem cupidatat minim incididunt consequat dolore qui do aliqua. Mollit aliquip Lorem ullamco cupidatat qui commodo cillum quis dolor ut sint ex. Ullamco duis veniam Lorem consectetur mollit minim culpa cupidatat non voluptate dolore commodo.\r\n",
    "registered": "2020-03-02T06:35:18 -01:00",
    "latitude": 25.199295,
    "longitude": 100.191129,
    "tags": [
      "ullamco",
      "Lorem",
      "reprehenderit",
      "aute",
      "esse",
      "non",
      "amet"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Rollins Burch"
      },
      {
        "id": 1,
        "name": "Pitts Rose"
      },
      {
        "id": 2,
        "name": "Good Rodgers"
      }
    ],
    "greeting": "Hello, Olive Hopper! You have 6 unread messages.",
    "favoriteFruit": "apple"
  },
  {
    "_id": "5fa3fd7fc57d89fe1c7856f2",
    "index": 4,
    "guid": "71a68831-fad1-4416-98f6-4a3934437fc8",
    "isActive": false,
    "balance": "$1,843.84",
    "picture": "http://placehold.it/32x32",
    "age": 35,
    "eyeColor": "blue",
    "name": "Becky Howe",
    "gender": "female",
    "company": "INSURETY",
    "email": "beckyhowe@insurety.com",
    "phone": "+1 (858) 435-3130",
    "address": "534 Glendale Court, Corriganville, Missouri, 974",
    "about": "Officia consectetur ex fugiat laborum laborum fugiat minim ipsum id. Veniam in sit non culpa esse aliquip deserunt proident dolore. Ad ipsum sit eiusmod sunt occaecat id esse id. Cillum aliqua sint non tempor excepteur. Ullamco exercitation dolor non tempor reprehenderit in. Occaecat consequat non anim adipisicing eiusmod. Fugiat enim fugiat ullamco occaecat eu commodo laborum commodo est amet.\r\n",
    "registered": "2015-03-09T02:59:47 -01:00",
    "latitude": 36.732737,
    "longitude": -159.588004,
    "tags": [
      "nulla",
      "nisi",
      "excepteur",
      "Lorem",
      "irure",
      "magna",
      "ullamco"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Jarvis Guy"
      },
      {
        "id": 1,
        "name": "Emma Mcdonald"
      },
      {
        "id": 2,
        "name": "Dickson Pope"
      }
    ],
    "greeting": "Hello, Becky Howe! You have 8 unread messages.",
    "favoriteFruit": "banana"
  }
]
        }
    },

    head() {
      return {
        title: "Registracije u tijeku"
      };
    }
}
</script>

<style>
  .root {
    height: 100%;
    width: 100%;
    margin: auto;
    background-position: center;
    background-size: cover;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('~@/static/images/terminko1.jpg');
    position: absolute;
    box-sizing: border-box;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  table {
    display: grid;
    grid-template-columns: minmax(150px, 2fr) minmax(150px, 1fr) minmax(150px, 2fr);
    grid-template-rows: 50px;
    margin: 6% 20%;
    background: #fff;
    height: 480px;
    /* padding: 15px; */
    overflow: hidden;
    border-collapse: collapse;
    /* min-width: 100%; */
  }

  thead, tbody, tr {
    display: contents;
  }
  
  th, td {
    padding: 15px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th {
    position: sticky;
    top: 0;
    background: #4e43e2;
    /* text-align: left; */
    font-weight: normal;
    font-size: 1.1rem;
    color: white;
  }


  td {
    padding-top: 10px;
    padding-bottom: 10px;
    color: #262626 ;
  }

  tr:nth-child(even) td {
    background: #f8f6ff;
  }
  
  #myBtn {
    width: 120px;
    background: linear-gradient(to right, #4e43e2, #4fdee6);
    border-radius: 30px;
    transition: .5s;
    border: 0;
    outline: none;
    color: #262626 ;
  }
  .show_btn {
    display: contents;
  }
  .hide_btn {
    display: none;
  }
</style>