class DocumentTemplate:
    def __init__(self):
        pass

    @staticmethod
    def create_db_template(server, db_id, label, **kwargs):
        db_url = f"{server}{db_id}"
        comment = kwargs.get("comment")
        language = kwargs.get("language", "en")
        allow_origin = kwargs.get("allow_origin", "*")

        temp = {
            "@context": {
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "terminus": "http://terminusdb.com/schema/terminus#",
                "_": db_url,
            },
            "terminus:document": {
                "@type": "terminus:Database",
                "rdfs:label": {"@language": language, "@value": label},
                "terminus:allow_origin": {
                    "@type": "xsd:string",
                    "@value": allow_origin,
                },
                "@id": db_url,
            },
            "@type": "terminus:APIUpdate",
        }
        if comment:
            temp["rdfs:comment"] = {"@language": language, "@value": comment}
        return temp

        @staticmethod
        def format_document(doc, schema_url, options=None, url_id=None):
            document = {}
            if isinstance(doc, dict):
                document["@context"] = doc["@context"]
                # add blank node prefix as document base url
                if ("@context" in doc) and ("@id" in doc):
                    document["@context"]["_"] = doc["@id"]

                if (
                    options
                    and options.get("terminus:encoding")
                    and options["terminus:encoding"] == "terminus:turtle"
                ):
                    document["terminus:turtle"] = doc
                    # document['terminus:schema'] = schema_url
                    del document["terminus:turtle"]["@context"]
                else:
                    document["terminus:document"] = doc
                    del document["terminus:document"]["@context"]

                document["@type"] = "terminus:APIUpdate"

                if url_id:
                    document["@id"] = url_id

            return document
