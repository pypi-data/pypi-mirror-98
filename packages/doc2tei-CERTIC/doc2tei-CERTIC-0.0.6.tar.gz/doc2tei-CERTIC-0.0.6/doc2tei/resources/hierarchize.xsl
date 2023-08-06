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
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"		
  exclude-result-prefixes="">
    
<xsl:output method="xml" encoding="UTF-8" indent="yes"/>

<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<!-- Match sur le corps du document, on ne touche pas au reste. On active le traitement sur le niveau de titre le plus haut (0) -->
<xsl:template match="office:body">
  <div type="article">
    <xsl:for-each-group select="*" group-starting-with="text:h[@text:outline-level=0]">
        <xsl:call-template name="addDiv">
          <xsl:with-param name="level" select="1"/>
          <xsl:with-param name="currentGroup" select="current-group()"/>
        </xsl:call-template>
    </xsl:for-each-group>
  </div>
</xsl:template>

<!-- Pour chaque groupe commençant par un text:h, on relance le traitement en passant le niveau en paramètre. Si le groupe courant contient un text:h du niveau souhaité, le traitement se poursuit, sinon il s'arrête -->
<xsl:template name="addDiv">
  <xsl:param name="level"/>
  <xsl:param name="currentGroup"/>

  <xsl:for-each-group select="$currentGroup" group-starting-with="text:h[@text:outline-level=$level]">
    <xsl:choose>
      <xsl:when test="self::text:h[@text:outline-level=$level]">
        <div type="section{$level}">
          <xsl:call-template name="addDiv">
            <xsl:with-param name="level" select="$level+1"/>
            <xsl:with-param name="currentGroup" select="current-group()"/>
          </xsl:call-template>
        </div>                  
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="current-group()"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each-group>      
  
</xsl:template>


</xsl:stylesheet>
