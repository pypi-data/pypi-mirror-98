(snowmobile.toml)=
# *snowmobile.toml*
<hr class="sn-grey">
<div class="sn-link-container2">
<a 
    class="sphinx-bs badge badge-primary text-white reference external sn-api" 
    href="../autoapi/snowmobile/core/configuration/index.html" 
    title="API Documentation">
        <span>snowmobile.core.configuration</span>
</a>
<a 
    class="sphinx-bs badge badge-primary text-white reference external sn-api" 
    href="../autoapi/snowmobile/core/cfg/index.html" 
    title="API Documentation">
        <span>snowmobile.core.cfg</span>
</a>
</div>

The parsed and validated form of [snowmobile.toml](#snowmobiletoml) is a 
{class}`~snowmobile.core.configuration.Configuration` object. 

All parsing of the file is done within {mod}`snowmobile.core.cfg`, in which 
sections are split at the root and fed into {xref}`pydantic's` glorious 
API to define the schema and impose (evolving) validation where needed.

Once validated, the {class}`~snowmobile.core.Configuration` object serves as a 
namespace for the contents/structure of the configuration file and utility 
methods implemented on top of them, with the rest of the API accessing it as the 
{attr}`~snowmobile.Snowmobile.cfg` attribute of
<a class="fixture-sn" href="../index.html#fixture-sn"></a>.


<hr class="sn-grey">
<hr class="sn-spacer-thick">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(inspecting-cfg)=
### Inspecting {attr}`sn.cfg`
<hr class="sn-green-thick-g">

````````{div} sn-tabbed-section

 ```````{tabbed} &nbsp;
 ```{div} sn-pre-code-s
 The {class}`~snowmobile.Configuration` model is accessed as the 
 {attr}`~snowmobile.Snowmobile.cfg`
 attribute of {class}`~snowmobile.Snowmobile`; a straight-forward way to inspect
 its composition is to instantiate
 a [delayed instance](./snowmobile.md#delaying-connection) of
 <a class="fixture-sn" href="../index.html#fixture-sn"></a>: 
 ```
 ```{literalinclude} ../snippets/configuration/inspect_configuration.py
 :language: python
 :lines: 5-10
 ```
 
 ```{div} sn-pre-code-s 
 The following attributes of `sn.cfg` map to the root configuration 
 sections of [](#snowmobiletoml):
 ```
 ```{literalinclude} ../snippets/configuration/inspect_configuration.py
 :language: python
 :lines: 12-16
 ```
 
 ```{div} sn-snippet
 [{fa}`file-code-o` inspect_configuration.py](../snippets.md#inspect_configurationpy)
 ```
 
 ```{admonition} Tip
 :class: tip
 Most root sections of [snowmobile.toml](#snowmobiletoml) outlined above map
 directly to a {xref}`snowmobile` object, the documentation for which contains 
 more detailed information on its configuration and associated application.
 ```
 ```````

````````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(connection.root)=
## Glossary
<hr class="sn-green-thick">

<br>

+++++++++++++
+++++++++++++
+++++++++++++
`````{tabbed} [connection]
 :new-group:
 (connection.default-creds)=
 *Configuration options
 used by* <a class="fixture-sn" href="../index.html#fixture-sn"></a> 
 *when establishing connections to {xref}`snowflake`*
 
`````

+++++++++++++
`````{tabbed} default-creds
 :new-group:
 (connection.credentials)=
 *The credentials (alias) to use by default in absence of one provided to
 the* `creds` *keyword argument to {meth}`snowmobile.connect()`*
`````

+++++++++++++
`````{tabbed} [connection.credentials]
 :new-group:
 (connection.credentials.creds1)=
 *Groups subsections of credentials, each declared with the structure of
 ``[connection.credentials.credentials_alias]``*
`````
`````{tabbed} +
 The value of `credentials_alias` is the literal string to pass to the
 ``creds`` argument of {meth}`snowmobile.connect()` to establish the
 {xref}`snowflake` connection with those credentials.
 
 Additional, non-credential keyword-arguments can be specified in an aliased 
 section if included **verbatim** as they should be passed to
 {xref}`snowflake.connector.connect()`; this can be used to to map
 a specific timezone or transaction mode (for example) to a specific set of
 credentials.
`````

+++++++++++++
`````{tabbed} [connection.credentials.creds1]
 :new-group:
 (connection.credentials.creds2)=
 *Store your first set of credentials here;* `creds1` *is a credentials alias*
`````

+++++++++++++
`````{tabbed} [connection.credentials.creds2]
 :new-group:
 (connection.default-arguments)=
 *Store as many credentials as you want following this format; aliases must be unique*
`````

+++++++++++++
`````{tabbed} [connection.default-arguments]
 :new-group:
 (loading.root)=
 *Default, non-credential keyword arguments to be passed to {xref}`snowflake.connector.connect()`*
`````
`````{tabbed} +
 Any arguments in this section that overlap with those stored in an aliased
 credentials block will be superceded by those associated with the credentials.
`````

+++++++++++++
+++++++++++++
+++++++++++++
`````{tabbed} [loading]
 :new-group:
 (loading.default-table-kwargs)=
 *Configuration options for data loading used by [snowmobile.Table](./table)*
`````

+++++++++++++
`````{tabbed} [loading.default-table-kwargs]
 :new-group:
 (loading.put)=
 *Default specifications for a* [**snowmobile.Table**](./table.ipynb) *object*
`````
`````{tabbed} Details: file_format
 The `file_format` option groups together aliases for:
    1.  An **in-warehouse** file format
    2.  A set of {ref}`[loading.save-options]<loading.save-options>`
    3.  A statement name for the DDL that creates this file format if it's
        called on and doesn't yet exist in the current schema (managed by
        [snowmobile.Table](./table)
`````

+++++++++++++
`````{tabbed} [loading.put]
 :new-group:
 (loading.copy-into)=
 *Default arguments to include in Snowflake's {xref}`put file from stage` command*
`````

+++++++++++++
`````{tabbed} [loading.copy-into]
 :new-group:
 (loading.save-options)=
 *Default arguments to include in Snowflake's {xref}`copy into table` command*
`````

+++++++++++++
`````{tabbed} [loading.save-options]
 :new-group:
 (loading.save-options.snowmobile_default_csv)=
 *Groups subsections of save-options*
`````

+++++++++++++
`````{tabbed} [loading.save-options."snowmobile_default_csv"]
 :new-group:
 (loading.save-options.snowmobile_default_psv)=
 *Default file-save options for **snowmobile_default_csv***
`````
`````{tabbed} +
 This defines a set of keyword arguments associated with the file format
 `snowmobile_default_csv` to be passed directly to the 
 {meth}`df.to_csv()<pandas.DataFrame.to_csv>` method when exporting
 data to a local file in advance of using Snowflake's {xref}`put file from stage` 
 command to load it into a staging table.
`````

+++++++++++++
`````{tabbed} [loading.save-options."snowmobile_default_psv"]
 :new-group:
 (external-sources.root)=
 *Default file-save options for **snowmobile_default_psv***
`````
`````{tabbed} +
 *These options mirror those of*
 [snowmobile_default_csv](loading.save-options.snowmobile_default_csv) except 
 that the delimiter is a pipe as opposed to a comma* 
`````


+++++++++++++
+++++++++++++
+++++++++++++
`````{tabbed} [external-sources]
 :new-group:

 (script.root)=
 *Defines paths to custom sources referenced by different {xref}`snowmobile` objects*

 ```{div} sn-def
  `ddl`\
  *Posix path to a sql file containing DDL for file formats*

  `extension`\
  *Posix path to [snowmobile-ext.toml](file-contents-snowmobile-ext-toml)*
 ```
`````

+++++++++++++
+++++++++++++
+++++++++++++
`````{tabbed} [script]
 :new-group:
 (script.save-dir-name)=
 *Configurations for [*snowmobile.Script*](./script.ipynb)*
`````

+++++++++++++
`````{tabbed} save-dir-name
 :new-group:
 (script.patterns.core)=
 *Directory name for generated exports (markup and stripped sql scripts)* 
`````

+++++++++++++
`````{tabbed} [script.patterns.core]
 :new-group:

 (script.patterns.wildcards)=
 *Core patterns used for markup identification*

 ```{div} sn-def
 `open-tag`\
 *Open-pattern for in-script tags*
 
 `close-tag`\
 *Close-pattern for in-script tags*
 
 `description-delimiter`\
 *Delimiter separating description from other statement attributes*
 
 `description-index-prefix`\
 *String with which to prepend a statement's index position when deriving 
 {attr}`~snowmobile.core.name.Name.desc_ge`*
 ```
`````

+++++++++++++
`````{tabbed} [script.patterns.wildcards]
 :new-group:

 (script.qa)=
 *Defines wildcards for attribute names within script tags*

 ```{div} sn-def
 `wildcard-character`\
 *The literal character to use as a wildcard*
 
 `wildcard-delimiter`\
 *The literal character with which to delimit wildcards*
 
 `denotes-paragraph`\
 *Indicates the attribute **value** should be rendered as free-form markdown as opposed to a plain text bullet*
 
 `denotes-no-reformat`\
 *Indicates the attribute **name** should be left exactly as it is entered in the script as opposed to title-cased*
 
 `denotes-omit-name-in-output`\
 *Indicates to omit the attribute's **name** in rendered output*
 ```
`````

+++++++++++++
`````{tabbed} [script.qa]
 :new-group:

 (script.qa.default-tolerance)=
 *Default arguments for **QA-Diff** and **QA-Empty** Statements*

 ```{div} sn-def
  `partition-on`\
  *Pattern to identify the field on which to partition data for comparison*

  `compare-patterns`\
  *Pattern to identify fields being compared*

  `ignore-patterns`\
  *Pattern to identify fields that should be ignored in comparison*

  `end-index-at`\
  *Pattern to identify the field marking the last index column*
 ```
`````

+++++++++++++
`````{tabbed} [script.qa.default-tolerance]
 :new-group:

 (script.markdown)=
 *Default values for QA-Delta tolerance levels*

 ```{div} sn-def
  `relative`\
  *Default relative-difference tolerance*

  `absolute`\
  *Default absolute-difference tolerance*
 ```
`````

+++++++++++++
`````{tabbed} [script.markdown]
 :new-group:

 (script.markdown.attributes)=
 *Configuration for markdown generated from .sql files*

 ```{div} sn-def
  `default-marker-header`\
  *Header level for [markers](./script.ipynb#markers) (h1-h6)*

  `default-statement-header`\
  *Header level for statements (h1-h6)*

  `default-bullet-character`\
  *Character to use for bulleted lists*

  `wrap-attribute-names-with`\
  *Character to wrap attribute **names** with*

  `wrap-attribute-values-with`\
  *Character to wrap attribute **values** with*

  `include-statement-index-in-header`\
  *Denotes whether or not to include a statement's relative index number in its header along with its name*

  `limit-query-results-to`\
  *Maximum number of rows to include for a statement's rendered **Results***
 ```
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes]
 :new-group:
 (script.markdown.attributes.markers)=
 *Configuration options for specific attributes*
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.markers]
 :new-group:
 (script.markdown.attributes.script)=
 *Pre-defined marker configurations*
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.markers."\\_\\_script\\_\\_"]
 :new-group:

 (script.markdown.attributes.markers.appendix)=
 *Scaffolding for a template marker called '\_\_script\_\_'*

 ```{div} sn-def
  `as-group`\
  *The literal text within which to group associated attributes as sub-bullets*

  `team`\
  *A sample attribute called 'team'*

  `author-name`\
  *A sample attribute called 'author-name'*

  `email`\
  *A sample attribute called 'email'*
 ```
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.markers."\\_\\_appendix\\_\\_"]
 :new-group:
 (script.markdown.attributes.reserved.rendered-sql)=
 *Scaffolding for a second template marker called '\_\_appendix\_\_'*
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.reserved.rendered-sql]
 :new-group:

 (script.markdown.attributes.reserverd.query-results)=
 *Configuration options for a reserved attribute called 'rendered-sql'*

 ```{div} sn-def
  `include-by-default`\
  *Include attribute by default for each {class}`~snowmobile.core.Section`*

  `attribute-name`\
  *The attribute's name as it is declared within a [tag](./script.md#tags)*

  `default-to`\
  *The attribute name as it should be interpreted when parsed*
 ```
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.reserved.query-results]
 :new-group:

 (script.markdown.attributes.from-namespace)=
 *Configuration for a reserved attributes called `query-results`*

 ```{div} sn-def
  `include-by-default`\
  *Include attribute by default for each {class}`~snowmobile.core.Section`*

  `attribute-name`\
  *The attribute's name as it is declared within a [tag](./script.md#tags)*

  `default-to`\
  *The attribute name as it should be interpreted when parsed*

  `format`\
  *Render format for the tabular results; markdown or html*
 ```
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.from-namespace]
 :new-group:
 (script.markdown.attributes.groups)=
 *List of {class}`~snowmobile.core.Statement` attributes to include in 
 its {class}`~snowmobile.core.Section`; includes non-default attributes
 set on an instance*
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.groups]
 :new-group:
 (script.markdown.attributes.order)=
 *Defines attributes to be grouped together within a sub-bulleted list*
`````

+++++++++++++
`````{tabbed} [script.markdown.attributes.order]
 :new-group:
 (script.tag-to-type-xref)=
 *Order of attributes within a {class}`~snowmobile.core.Statement`-level section*
`````

+++++++++++++
`````{tabbed} [script.tag-to-type-xref]
 :new-group:
 
 (sql.root)=
 *Maps tagged attributes to data types; will error if an attribute included here
 cannot be parsed into its specified data type*
`````

+++++++++++++
`````{tabbed} [sql]
 :new-group:
 :class-label: sn-ext
 
 (file-contents-ref)=
 *SQL parsing specifications for a {class}`~snowmobile.core.Statement`*

 ```{div} sn-def
  (desc-is-simple)=
  `provided-over-generated`\
  *{class}`~snowmobile.core.name.Name.nm_pr` 
  takes precedent over {class}`~snowmobile.core.name.Name.nm_ge`*

  (named-objects)=  
  `desc-is-simple`\
  *`True` invokes additional parsing into {class}`~snowmobile.core.name.Name.desc` 
  and {class}`~snowmobile.core.name.Name.obj`*

  (generic-anchors)=
  `named-objects`\
  *Literal strings to search for matches that qualify as a {xref}`snowflake`
  object if included within the first line of a statement's sql and not equal
  to its first keyword*

  (keyword-exceptions)=
  `generic-anchors`\
  *Generic anchors to use for a given keyword; will be used for generated statements
  if* `desc-is-simple` *is* **True**
  
  (information-schema-exceptions)=
  `keyword-exceptions`\
  *Alternate mapping for first keyword found in a command*
  
  `information-schema-exceptions`\
  *Map {xref}`snowflake` objects to their `information_schema.*` table name
  if different than the plural form of the object; (e.g. `schema` information 
  is in `information_schema.schemata` not `information_schema.schemas`)*
 ```
 
`````

<hr class="sn-spacer-thick2">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## File Contents
<hr class="sn-green-thick">

```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile-template.toml
:language: toml
:lineno-start: 1
```

<hr class="sn-spacer-thick2">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(file-contents-snowmobile-ext-toml)=
## snowmobile-ext.toml
<hr class="sn-green-thick">

```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile-ext.toml
:language: toml
:lineno-start: 1
```


% indentation for glossary
<style>

.md-typeset .tabbed-set.docutils {
    margin-top: 0;
    margin-bottom: -0.5rem;
}

.sn-dedent-v-container .tabbed-content.docutils  {
    margin-bottom: -0.5em;
}

.sn-def :last-child {
    margin-bottom: -0.2em;
}

.tabbed-content.docutils {
    padding-left: 1rem;
    margin-bottom: 0.5rem;
    border-top: unset;
}

.tabbed-content {
    box-shadow: none;
}

@media only screen and (max-width: 59.9375em) {
    .tabbed-set>label {
        padding: 0.8rem 0.1rem 0;
    }
}
</style>
