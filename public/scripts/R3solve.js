let addData = function (data, collecxn) {
  const collection = firebase.firestore().collection(collecxn.toString());
  return collection.add(data);
};

let getNDocuments = function (collection, n, process) {
  const query = firebase.firestore()
    .collection(collection.toString())
    .limit(n);
  getDocumentsInQuery(query, process);
};

let getDocumentsInQuery = function (query, process) {
  query.onSnapshot((snapshot) => {
    if (!snapshot.size) {
      return process();
    }

    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added' || change.type === 'modified') {
        process(change.doc);
      }
    });
  });
};

let getDocument = function (id, collection) {
  return firebase.firestore().collection(collection.toString()).doc(id).get();
};

let getFilteredDocuments = function (filters, collection, process) {
  let query = firebase.firestore().collection(collection.toString());

  if (filters.count !== 'Any') {
    query = query.where('count', '==', filters.count);
  }

  if (filters.name !== 'Any') {
    query = query.where('name', '==', filters.name);
  }

  getDocumentsInQuery(query, process);
};

let addDocument = function (collecxn, data) {
  const newDocument = document.collection(collecxn).doc();

  return firebase.firestore().runTransaction((transaction) => {
    return transaction.set(newDocument, data);
  });
};

let processDoc = function(doc) {
    if (!doc) {
        console.log("processDoc got no doc.");
        return;
    }
    console.log("processDoc got doc.");
    var data = doc.data();
    console.log(doc.id,":",data);
}

window.onload = function() {
    /*firebase //WORKS!
    .firestore()
    .collection('categories')
    .limit(2)
    .onSnapshot(function(snapshot) {
        if (snapshot.empty) {
            console.log("Snapshot is empty.");
        } else {
            console.log("Snapshot is not empty.");
            snapshot.forEach(function (doc) {
                console.log(doc.id.toString(),":",doc.data());
            })
        }
    });*/
    //console.log("HERE");
    //getNDocuments('categories', 2, processDoc);
    //console.log("HERE");
    let app;
    try {
        app = firebase.app();
        if (window.document.title == "R3solve") {
            var db = app.firestore();
            var collection = db.collection("categories");
            collection.limit(5).get().then(function(docs) {
                let content = "";
                docs.forEach(function(doc) {
                    console.log(doc.id, " => ", doc.data());
                    content += '<a href="#" class="list-group-item list-group-item-action">'
                    content += doc.data().name.toString();
                    content += '</a>'
                });
                document.getElementById('top-problems').innerHTML = content;
            }).catch(function(error) {
                console.log("Error executing query:", error);
            });
        }
    } catch (e) {
        console.error(e);
    }
};
