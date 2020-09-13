let addCategory = function (data) {
  const collection = firebase.firestore().collection('categories');
  return collection.add(data);
};

let getAllCategories = function (render) {
  const query = firebase.firestore()
    .collection('categories')
    .orderBy('count', 'desc')
    .limit(5);
  this.getDocumentsInQuery(query, render);
};

let getDocumentsInQuery = function (query, render) {
  query.onSnapshot((snapshot) => {
    if (!snapshot.size) {
      return render();
    }

    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added' || change.type === 'modified') {
        render(change.doc);
      }
    });
  });
};

let getCategory = function (id) {
  return firebase.firestore().collection('categories').doc(id).get();
};

let getFilteredCategories = function (filters, render) {
  let query = firebase.firestore().collection('categories');

  if (filters.count !== 'Any') {
    query = query.where('count', '==', filters.count);
  }

  if (filters.name !== 'Any') {
    query = query.where('name', '==', filters.name);
  }

  this.getDocumentsInQuery(query, render);
};

let addTag = function (categoryID, tag) {
  const collection = firebase.firestore().collection('categories');
  const document = collection.doc(categoryID);
  const newDocument = document.collection('tags').doc();

  return firebase.firestore().runTransaction((transaction) => {
    return transaction.get(document).then((doc) => {
      const data = doc.data();

      transaction.update(document, {
        test: 17,
        result: true
      });
      return transaction.set(newDocument, tag);
    });
  });
};

let renderResults = function(doc) {
    if (!doc) {
        console.log("renderResults got no doc.");
        return;
    }
    console.log("renderResults got doc.");
    var data = doc.data();
    data['.id'] = doc.id;
    console.log(doc.id,":",data);
}

window.onload = function() {
    firebase
    .firestore()
    .collection('categories')
    .limit(1)
    .onSnapshot(function(snapshot) {
        if (snapshot.empty) {
            console.log("Snapshot is empty.");
        } else {
            console.log("Snapshot is not empty.");
        }
    });
    
    getAllCategories(renderResults);

    let app;
    try {
        app = firebase.app();
    } catch (e) {
        console.error(e);
    }
    let user = {
        id: "3kvjG9Bjy1dQKWwA8Tzs"
    };
    if (app) {
        var db = app.firestore();
        var collection = db.collection("users");
        collection.doc(user.id).get().then(function(docs) {
            if (docs) {
                console.log("Success:", docs.data());
            } else {
                console.log("Empty result.");
            }
        }).catch(function(error) {
            console.log("Error executing query:", error);
        });
    } else {
        console.log("Something's wrong...");
    }
};
