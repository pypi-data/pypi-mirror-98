<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:
  xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:
  xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:
  xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:
  xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:
  xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:
  xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:
  xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:
  xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:
  xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:
  xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:
  xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"		
  exclude-result-prefixes="">
    
<xsl:output method="xml" encoding="UTF-8" indent="no"/>

<!-- ### On clean mais on ne simplifie pas ### -->
    
<!-- ### CLEANUP.XSL objectifs et description

À l'issue de cette transformation :

* Niveaux de titres
- le titre principal du document est ramené à un élément text:h[@text:outline-level='0'] (sources MS Word ou Libre Office) ;
- les niveaux de titres pour constuire l'arborescence sont ensuite uniformément balisés : <text:h> avec un attribut @text:outline-level associé ;
* Attributs
- tous les attributs sont conservés (<xsl:copy-of select="@*"/>) ;
* Enrichissements typographiques
- les raccourcis vers les enrichissements typographiques et leurs propriétés sont ramenés à la liste des propriétés, séparés par un espace (token) ;
- liste des propriétés conservées : italique, gras, exposant, indice, souligné, barré, petites-capitales (+ combinaison) ;
* Nettoyage
- suppression des éléments hérités du logiciel, des caractères de saut, par défaut… (voir liste infra) ;
- suppression de l'exposant autour des éléments de notes ;

Prérequis dans la construction du modèle de stylage : 
- pas d'héritage dans la création du style ;

XSL auxiliaire : 
- extract_style-name.xsl (extraction des @text:style-name)

Q & Remarques : 
- gestion des namespaces ;
- double-barré double-souligné à traiter (?)

Todo (ec)
- ajouter une préparation des tableaux, des listes (<text:list @xml:id text:style-name="WW8Num3">) ?
- suppression des sections 
    - voir fichier Franco Bruni)
    - voir modalités de traitements des annexes et bibliographies
- style Footnote (style natif de Word) basé sur Standard…
- supprimer les paragraphes vides ?
- gestion des erreurs : cas de deux titres principaux OU pass 2 : si pas de outline-level=0 que faire ?
- /!\ Titre-section-biblio et Titre-section-annexe

* Suite ?
- table d'équivalence des noms de styles pour les ramener à un intitulé unique
-->
    
<!-- suppression/nettoyage -->
<!-- données traitement de texte -->
<xsl:template match="office:settings"/>
<xsl:template match="office:scripts"/>
<xsl:template match="office:font-face-decls"/>
<xsl:template match="office:styles"/>
<xsl:template match="office:automatic-styles"/>
<xsl:template match="office:master-styles"/>
<xsl:template match="office:text/text:sequence-decls"/>
<xsl:template match="office:forms"/>
<!-- caractères de saut, tabulations -->
<xsl:template match="text:soft-page-break"/>
<xsl:template match="text:tab"/>
<xsl:template match="text:s"/> <!-- This element shall be used to represent the second and all following “ “ (U+0020, SPACE) characters in a sequence of “ “ (U+0020, SPACE) characters. -->
<!-- ancres par défaut -->
<xsl:template match="text:bookmark[starts-with(@text:name,'_')]"/>
<!-- images en binaire -->
<xsl:template match="office:binary-data"/>
<!-- élément engloblant office:text (à conserver pour génération de la mainDiv) -->
<!-- A priori office:body est toujours présents dans les fichiers. office:text n'est plus à conserver pour génération de la mainDiv-->
<xsl:template match="office:text">
  <xsl:apply-templates/>
</xsl:template>
    
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>
    

<!-- Gestion des raccourcis de styles -->
<xsl:template match="*[@text:style-name]">
    
  <xsl:variable name="currentStyle">
    <xsl:value-of select="@text:style-name"/>
  </xsl:variable>
  <xsl:variable name="currentElementName">
    <xsl:value-of select="name(.)"/>
  </xsl:variable>

<xsl:choose>
    <!-- Suppression des éléments vides -->
    <xsl:when test=".[not(*|comment()|processing-instruction()) and normalize-space()='']"/>
    <!-- Gestion des enrichissements typographiques text:span -->
    <xsl:when test="$currentElementName='text:span'">
        <xsl:choose>
        <!-- enrichissements typo traitement de texte (l'application de styles de caractères ne génère pas de raccourcis de styles)-->
            <xsl:when test="matches(@text:style-name,'[T]\d{1,2}')">
                <xsl:choose>
                    <!-- premier test pour une liste des propriétés retenus -->
                    <xsl:when test="//style:style[@style:name=$currentStyle]/style:text-properties/(@fo:font-style|@fo:font-variant|@fo:font-weight|@style:text-position|@style:text-underline-style)">
                    <xsl:element name="text:span">
                        <xsl:attribute name="rendition">
                        <!-- ajouter le rtl -->
                        <!-- liste fermée des cas à traiter -->
                        <xsl:for-each select="//style:style[@style:name=$currentStyle]/style:text-properties/(@fo:font-style|@fo:font-variant|@fo:font-weight)">
                            <xsl:if test="./position()!=last()">
                                <xsl:text> </xsl:text>
                            </xsl:if>
                            <xsl:value-of select="."/>
                        </xsl:for-each>
                        <xsl:for-each select="//style:style[@style:name=$currentStyle]/style:text-properties/@style:text-position">
                            <xsl:if test="//style:style[@style:name=$currentStyle]/style:text-properties/(@fo:font-style|@fo:font-variant|@fo:font-weight)"><xsl:text> </xsl:text></xsl:if>
                            <xsl:choose>
                                <xsl:when test="contains(.,'super')">
                                    <xsl:text>sup</xsl:text>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="substring-before(.,' ')"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>
                        <xsl:for-each select="//style:style[@style:name=$currentStyle]/style:text-properties/@style:text-underline-style">
                            <xsl:if test="//style:style[@style:name=$currentStyle]/style:text-properties/(@fo:font-style|@fo:font-variant|@fo:font-weight|@style:text-position)"><xsl:text> </xsl:text></xsl:if>
                            <xsl:text>underline</xsl:text>
                        </xsl:for-each>
                        <xsl:for-each select="//style:style[@style:name=$currentStyle]/style:text-properties/@style:text-line-through-style">
                            <xsl:text>line-through</xsl:text>
                        </xsl:for-each>                
                        </xsl:attribute>
                        <xsl:apply-templates/>
                    </xsl:element>
                    </xsl:when>
                    <!-- dans les autres cas, on ne souhaite pas retenir les propriétés -->
                    <xsl:otherwise>
                        <xsl:apply-templates/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="@text:style-name='apple-converted-space'">
                <xsl:text> </xsl:text><xsl:apply-templates/>
            </xsl:when>
            <!-- neutralisation des styles hérités et identifiés -->
            <xsl:when test="starts-with(@text:style-name,'apple') or starts-with(@text:style-name,'Internet_') or starts-with(@text:style-name,'Placeho')">
                <xsl:apply-templates/>
            </xsl:when>
            <!-- style de caractères appliqués -->
<!-- changement de logique : au lieu de supprimer les styles en trop, on ne conserve que les styles dont on connaît le préfixe (métopes ou oe) -->
            <xsl:otherwise>
                <xsl:copy-of select="."/>
                <!-- ne règle pas le problème d'imbrication de span… dans des liens hypertextes par exemple ; tester pour les doubles enrichissements typographiques aussi -->
<!--                <xsl:apply-templates/>-->
            </xsl:otherwise>
        </xsl:choose>
    </xsl:when>
    <!-- Gestion des titres (dont la gestion niveaux @text:outline-level) -->
    <xsl:when test="$currentElementName='text:h' or ($currentElementName='text:p' and @text:outline-level)">
        <xsl:element name="text:h">
            <xsl:copy-of select="@*"/>
            <xsl:attribute name="text:style-name">
                <xsl:choose>
                    <xsl:when test="matches($currentStyle,'[P]\d{1,2}')">
                        <xsl:value-of select="//style:style[@style:name=$currentStyle]/@style:parent-style-name"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$currentStyle"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:choose>
                <!-- Sur le titre principal (@text:outline-level="Title…"), on affecte un @text:outline-level à 0  -->
                <xsl:when test="starts-with($currentStyle,'Title') or starts-with(//style:style[@style:name=$currentStyle]/@style:parent-style-name,'Title')">
                    <xsl:attribute name="text:outline-level">0</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="@text:outline-level"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:when>
    <!-- Gestion du titre principale si source Libre Office : conversion de text:p à text:h  (à voir si besoin d'être conservé, car on peut affecter un niveau de plan via la stylage dans Libre Office) -->
    <xsl:when test="$currentElementName='text:p' and (@text:style-name='Title' or //style:style[@style:name=$currentStyle]/@style:parent-style-name='Title')">
        <xsl:element name="text:h">
            <xsl:copy-of select="@*"/>
            <xsl:attribute name="text:outline-level">0</xsl:attribute>
            <xsl:attribute name="text:style-name">
                <xsl:choose>
                    <xsl:when test="matches($currentStyle,'[P]\d{1,2}')">
                        <xsl:value-of select="//style:style[@style:name=$currentStyle]/@style:parent-style-name"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$currentStyle"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:when>
    <!-- Gestion des autres éléments -->
    <xsl:otherwise>
        <xsl:element name="{$currentElementName}">
            <xsl:copy-of select="@*"/>
            <xsl:attribute name="text:style-name">
                <xsl:choose>
                    <!-- est-ce qu'on estime que le système de nommage des raccourcis de styles est normalisé ? -->
                    <xsl:when test="matches($currentStyle,'[P]\d{1,2}')">
                        <xsl:value-of select="//style:style[@style:name=$currentStyle]/@style:parent-style-name"/>
                    </xsl:when>
                    <!-- cas d'un héritage de styles (paragraphes) -->
<!--                <xsl:when test="//style:style[@style:name=$currentStyle and @style:parent-style-name]">
                        <xsl:value-of select="//style:style[@style:name=$currentStyle]/@style:parent-style-name"/>
                    </xsl:when>  -->
                    <!-- style directement accessible -->
                    <xsl:otherwise>
                        <xsl:value-of select="$currentStyle"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:otherwise>
</xsl:choose>
</xsl:template>

</xsl:stylesheet>