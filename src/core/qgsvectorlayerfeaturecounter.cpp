#include "qgsvectorlayerfeaturecounter.h"

QgsVectorLayerFeatureCounter::QgsVectorLayerFeatureCounter( QgsVectorLayer *layer, const QgsExpressionContext &context )
  : QgsTask( tr( "Counting features in %1" ).arg( layer->name() ), QgsTask::CanCancel )
  , mSource( new QgsVectorLayerFeatureSource( layer ) )
  , mRenderer( layer->renderer()->clone() )
  , mExpressionContext( context )
  , mFeatureCount( layer->featureCount() )
{
  if ( !mExpressionContext.scopeCount() )
  {
    mExpressionContext = layer->createExpressionContext();
  }
}

bool QgsVectorLayerFeatureCounter::run()
{
  QgsLegendSymbolList symbolList = mRenderer->legendSymbolItems();
  QgsLegendSymbolList::const_iterator symbolIt = symbolList.constBegin();

  for ( ; symbolIt != symbolList.constEnd(); ++symbolIt )
  {
    mSymbolFeatureCountMap.insert( symbolIt->first, 0 );
  }

  // If there are no features to be counted, we can spare us the trouble
  if ( mFeatureCount > 0 )
  {
    int featuresCounted = 0;

    // Renderer (rule based) may depend on context scale, with scale is ignored if 0
    QgsRenderContext renderContext;
    renderContext.setRendererScale( 0 );
    renderContext.setExpressionContext( mExpressionContext );

    QgsFeatureRequest request;
    if ( !mRenderer->filterNeedsGeometry() )
      request.setFlags( QgsFeatureRequest::NoGeometry );
    request.setSubsetOfAttributes( mRenderer->usedAttributes( renderContext ), mSource->fields() );
    QgsFeatureIterator fit = mSource->getFeatures( request );

    // TODO: replace QgsInterruptionChecker with QgsFeedback
    // fit.setInterruptionChecker( mFeedback );

    mRenderer->startRender( renderContext, mSource->fields() );

    double progress = 0;
    QgsFeature f;
    while ( fit.nextFeature( f ) )
    {
      renderContext.expressionContext().setFeature( f );
      QSet<QString> featureKeyList = mRenderer->legendKeysForFeature( f, renderContext );
      Q_FOREACH ( const QString &key, featureKeyList )
      {
        mSymbolFeatureCountMap[key] += 1;
      }
      ++featuresCounted;

      double p = ( static_cast< double >( featuresCounted ) / mFeatureCount ) * 100;
      if ( p - progress > 1 )
      {
        progress = p;
        setProgress( progress );
      }

      if ( isCanceled() )
      {
        mRenderer->stopRender( renderContext );
        return false;
      }
    }
    mRenderer->stopRender( renderContext );
  }

  setProgress( 100 );

  emit symbolsCounted();
  return true;
}

QHash<QString, long> QgsVectorLayerFeatureCounter::symbolFeatureCountMap() const
{
  return mSymbolFeatureCountMap;
}

long QgsVectorLayerFeatureCounter::featureCount( const QString &legendKey ) const
{
  return mSymbolFeatureCountMap.value( legendKey, -1 );
}
